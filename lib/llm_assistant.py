"""LLM assistant utilities for Circuit Forge"""

import os
from typing import Any, Dict, List, Optional

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None

from lib.calculations import CircuitCalculator, BuckInputs
from lib.component_data import (MOSFET_LIBRARY, CAPACITOR_LIBRARY,
                                INDUCTOR_LIBRARY, INPUT_CAPACITOR_LIBRARY)
from lib.design_heuristics import list_all_design_documents

FUNCTION_SCHEMAS: List[Dict[str, Any]] = [
    {
        "name": "calculate_buck_components",
        "description": "Calculate key buck converter component values",
        "parameters": {
            "type": "object",
            "properties": {
                "v_in": {"type": "number", "description": "Maximum input voltage"},
                "v_out": {"type": "number", "description": "Desired output voltage"},
                "i_out": {"type": "number", "description": "Maximum output current"},
                "frequency": {"type": "number", "description": "Switching frequency in Hz"},
                "ripple_voltage": {"type": "number", "description": "Allowed output voltage ripple (V)"},
                "ripple_current": {"type": "number", "description": "Allowed inductor current ripple (A)"},
            },
            "required": ["v_in", "v_out", "i_out", "frequency", "ripple_voltage", "ripple_current"],
        },
    },
    {
        "name": "search_components",
        "description": "Search component database for matching part numbers or characteristics",
        "parameters": {
            "type": "object",
            "properties": {
                "component_type": {
                    "type": "string",
                    "enum": ["mosfet", "output_capacitor", "input_capacitor", "inductor"],
                },
                "filters": {"type": "object", "description": "Key/value filter pairs"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 10},
            },
            "required": ["component_type"],
        },
    },
    {
        "name": "explain_design_heuristic",
        "description": "Summarize available design heuristics documentation",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "MOSFETs, capacitors, or inductors"},
            },
            "required": [],
        },
    },
]


class LLMAgent:
    """LLM assistant that routes function calls"""

    def __init__(self, api_key: Optional[str] = None, functions: Optional[List[Dict[str, Any]]] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.functions = functions or FUNCTION_SCHEMAS

        if self.api_key and openai:
            openai.api_key = self.api_key

    def query(self, prompt: str, history: Optional[List[Dict[str, str]]] = None) -> str:
        history = history or []

        messages = [
            {"role": "system", "content": "You are an intelligent circuit design assistant."},
        ]

        messages.extend(history)
        messages.append({"role": "user", "content": prompt})

        if self.api_key and openai:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    temperature=0.2,
                    functions=self.functions,
                    function_call="auto",
                )

                choice = response.choices[0]
                message = choice.message

                if message.get("function_call"):
                    fn_call = message["function_call"]
                    return self._execute_function(fn_call)

                return message.get("content", "Sorry, I could not help right now.")

            except Exception as exc:
                return f"LLM request failed ({exc}). Please try again later."

        return self._fallback_response(prompt)

    def _execute_function(self, fn_call: Dict[str, Any]) -> str:
        name = fn_call.get("name")
        args = fn_call.get("arguments", {})

        if name == "calculate_buck_components":
            return _calculate_buck_components(**args)
        if name == "search_components":
            return _search_components(**args)
        if name == "explain_design_heuristic":
            return _explain_design_heuristic(**args)

        return "Function not supported."

    def _fallback_response(self, prompt: str) -> str:
        lower = prompt.lower()

        if "buck" in lower and "inductance" in lower:
            return _calculate_buck_components(
                v_in=48,
                v_out=5,
                i_out=10,
                frequency=100_000,
                ripple_voltage=0.05,
                ripple_current=1.0,
            )

        if "mosfet" in lower and "why" in lower:
            return "MOSFET recommendations leverage design heuristics in the `assets/design_heuristics` sets. Use the component library for detailed specs."

        return "This conversation requires an LLM function call. Please configure OPENAI_API_KEY to activate the assistant."


def _calculate_buck_components(
    v_in: float,
    v_out: float,
    i_out: float,
    frequency: float,
    ripple_voltage: float,
    ripple_current: float,
    **kwargs: Any,
) -> str:
    inputs = BuckInputs(
        v_in_min=v_in,
        v_in_max=v_in,
        v_out_min=v_out,
        v_out_max=v_out,
        p_out_max=v_out * i_out,
        efficiency=0.95,
        switching_freq=frequency,
        v_ripple_max=ripple_voltage,
        v_in_ripple=ripple_voltage / 2,
        i_out_ripple=ripple_current,
        v_overshoot=0.0,
        v_undershoot=0.0,
        i_loadstep=i_out * 0.2,
    )
    result = CircuitCalculator().calculate_buck(inputs)

    return (
        f"Buck Calculator Results:\n"
        f"• Inductance: {result.inductance:.2f} H\n"
        f"• Output Capacitance: {result.output_capacitance:.2f} F\n"
        f"• Input Capacitance: {result.input_capacitance:.2f} F\n"
        f"• Max Duty Cycle: {result.duty_cycle_max * 100:.1f}%"
    )


def _search_components(component_type: str, filters: Optional[Dict[str, Any]] = None, limit: int = 3) -> str:
    library = {
        "mosfet": MOSFET_LIBRARY,
        "output_capacitor": CAPACITOR_LIBRARY,
        "input_capacitor": INPUT_CAPACITOR_LIBRARY,
        "inductor": INDUCTOR_LIBRARY,
    }.get(component_type, [])

    filters = filters or {}
    matches = []

    for item in library:
        hit = True
        for key, value in filters.items():
            if not hasattr(item, key):
                hit = False
                break

            attr = getattr(item, key)
            if isinstance(value, (int, float)) and isinstance(attr, (int, float)):
                if attr < value:
                    hit = False
                    break
            elif isinstance(value, str) and value.lower() not in str(attr).lower():
                hit = False
                break

        if hit:
            matches.append(item)
        if len(matches) >= limit:
            break

    if not matches:
        return "No matching components found."

    response_lines = [f"Top {len(matches)} {component_type} results:"]
    for comp in matches:
        response_lines.append(f"• {getattr(comp, 'part_number', getattr(comp, 'name', 'Unknown'))} | {comp.manufacturer}")
    return "\n".join(response_lines)


def _explain_design_heuristic(topic: Optional[str] = None) -> str:
    docs = list_all_design_documents()
    topic = (topic or "general").lower()

    key_map = {
        "mosfet": "mosfets",
        "mosfets": "mosfets",
        "capacitor": "capacitors",
        "capacitors": "capacitors",
        "inductor": "inductors",
        "inductors": "inductors",
    }

    target = key_map.get(topic)

    if target and docs.get(target):
        descriptions = [f"• {os.path.basename(path)}" for path in docs[target][:3]]
        return "Available design heuristics for {}:\n".format(target.title()) + "\n".join(descriptions)

    summary = [f"{comp_type.title()}: {len(paths)} document(s)" for comp_type, paths in docs.items()]
    return "Available design heuristics:\n" + "\n".join(summary)
