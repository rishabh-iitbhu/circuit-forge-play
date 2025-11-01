import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';
import { SimulationReport, PermutationResult } from '@/types/permutation';

export function generatePDFReport(report: SimulationReport): void {
  const doc = new jsPDF();
  const pageWidth = doc.internal.pageSize.getWidth();
  
  // Title
  doc.setFontSize(20);
  doc.setFont('helvetica', 'bold');
  doc.text(`${report.circuitType} Circuit Simulation Report`, pageWidth / 2, 20, { align: 'center' });
  
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text(`Generated: ${new Date(report.timestamp).toLocaleString()}`, pageWidth / 2, 28, { align: 'center' });
  
  // Summary
  let yPos = 40;
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Simulation Summary', 14, yPos);
  
  yPos += 10;
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  doc.text(`Total Permutations Tested: ${report.permutations.length}`, 14, yPos);
  yPos += 6;
  doc.text(`Priority Metrics: ${report.priorityMetrics.join(', ')}`, 14, yPos);
  
  // Best Permutation
  yPos += 12;
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('Recommended Configuration', 14, yPos);
  
  yPos += 10;
  doc.setFontSize(10);
  doc.setFont('helvetica', 'normal');
  const best = report.bestPermutation;
  doc.text(`MOSFET: ${best.components.mosfet.part_number}`, 14, yPos);
  yPos += 6;
  doc.text(`Capacitor: ${best.components.capacitor.part_number}`, 14, yPos);
  yPos += 6;
  doc.text(`Inductor: ${best.components.inductor.part_number}`, 14, yPos);
  yPos += 6;
  doc.text(`Efficiency: ${(best.metrics.efficiency * 100).toFixed(2)}%`, 14, yPos);
  yPos += 6;
  doc.text(`Power Factor: ${best.metrics.powerFactor.toFixed(3)}`, 14, yPos);
  yPos += 6;
  doc.text(`THD: ${(best.metrics.thd * 100).toFixed(2)}%`, 14, yPos);
  
  // All Permutations Table
  doc.addPage();
  doc.setFontSize(14);
  doc.setFont('helvetica', 'bold');
  doc.text('All Permutations Comparison', 14, 20);
  
  const tableData = report.permutations.map(perm => [
    perm.rank || '-',
    perm.components.mosfet.part_number,
    perm.components.capacitor.part_number,
    perm.components.inductor.part_number,
    `${(perm.metrics.efficiency * 100).toFixed(2)}%`,
    perm.metrics.powerFactor.toFixed(3),
    `${(perm.metrics.thd * 100).toFixed(2)}%`
  ]);
  
  autoTable(doc, {
    head: [['Rank', 'MOSFET', 'Capacitor', 'Inductor', 'Efficiency', 'PF', 'THD']],
    body: tableData,
    startY: 30,
    styles: { fontSize: 8 },
    headStyles: { fillColor: [59, 130, 246] }
  });
  
  // Save
  doc.save(`${report.circuitType}_Simulation_Report_${Date.now()}.pdf`);
}

export function generateCSVReport(report: SimulationReport): void {
  const headers = [
    'Rank',
    'MOSFET',
    'Capacitor',
    'Inductor',
    'Efficiency (%)',
    'Power Factor',
    'THD (%)',
    'Voltage Ripple (V)',
    'Current Ripple (A)',
    'Peak Current (A)',
    'Score'
  ];
  
  const rows = report.permutations.map(perm => [
    perm.rank || '',
    perm.components.mosfet.part_number,
    perm.components.capacitor.part_number,
    perm.components.inductor.part_number,
    (perm.metrics.efficiency * 100).toFixed(2),
    perm.metrics.powerFactor.toFixed(3),
    (perm.metrics.thd * 100).toFixed(2),
    perm.metrics.voltageRipple.toFixed(2),
    perm.metrics.currentRipple.toFixed(2),
    perm.metrics.peakCurrent.toFixed(2),
    perm.score?.toFixed(4) || ''
  ]);
  
  const csvContent = [
    headers.join(','),
    ...rows.map(row => row.join(','))
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `${report.circuitType}_Simulation_Report_${Date.now()}.csv`;
  link.click();
}
