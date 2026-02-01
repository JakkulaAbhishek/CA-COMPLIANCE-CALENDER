/**
 * Comprehensive CA Compliance Calendar 2025-26
 * Includes: TDS, GST (Monthly/QRMP), PF/ESI, Advance Tax, and ITR.
 */

function setupComprehensiveCAEvents() {
  const calendar = CalendarApp.getDefaultCalendar();
  const year = 2025; // Setup for the 2025-26 cycle

  // 1. MONTHLY RECURRING EVENTS (Run for all 12 months)
  for (let month = 0; month < 12; month++) {
    const monthlyEvents = [
      { name: "TDS Payment", day: 7, desc: "Deposit TDS for previous month. (Note: March TDS due by April 30)" },
      { name: "GSTR-1 (Monthly)", day: 11, desc: "Filing of outward supplies for monthly filers" },
      { name: "PF & ESI Payment", day: 15, desc: "Provident Fund and ESI contribution deposit" },
      { name: "GSTR-3B (Monthly)", day: 20, desc: "Summary return & tax payment for monthly filers" }
    ];

    monthlyEvents.forEach(e => {
      // Special case: March TDS is due April 30
      let day = (e.name === "TDS Payment" && month === 2) ? 30 : e.day; 
      let targetMonth = (e.name === "TDS Payment" && month === 2) ? 3 : month;
      createComplianceEvent(calendar, e.name, new Date(year, targetMonth, day), e.desc);
    });
  }

  // 2. QUARTERLY EVENTS (TDS Returns & GST QRMP)
  const quarters = [
    { name: "TDS Return Filing (Q1)", date: new Date(2025, 6, 31), desc: "Form 24Q/26Q for April-June" },
    { name: "TDS Return Filing (Q2)", date: new Date(2025, 9, 31), desc: "Form 24Q/26Q for July-Sept" },
    { name: "TDS Return Filing (Q3)", date: new Date(2026, 0, 31), desc: "Form 24Q/26Q for Oct-Dec" },
    { name: "TDS Return Filing (Q4)", date: new Date(2026, 4, 31), desc: "Form 24Q/26Q for Jan-March" },
    { name: "GSTR-1 (QRMP)", months: [6, 9, 0, 3], day: 13, desc: "Quarterly GSTR-1 filing" }
  ];

  quarters.forEach(q => {
    if (q.date) {
      createComplianceEvent(calendar, q.name, q.date, q.desc);
    } else if (q.months) {
      q.months.forEach(m => createComplianceEvent(calendar, q.name, new Date(m > 5 ? 2025 : 2026, m, q.day), q.desc));
    }
  });

  // 3. ADVANCE TAX (4 Installments)
  const advTax = [
    { name: "Advance Tax - 1st (15%)", date: new Date(2025, 5, 15) },
    { name: "Advance Tax - 2nd (45%)", date: new Date(2025, 8, 15) },
    { name: "Advance Tax - 3rd (75%)", date: new Date(2025, 11, 15) },
    { name: "Advance Tax - 4th (100%)", date: new Date(2026, 2, 15) }
  ];
  advTax.forEach(t => createComplianceEvent(calendar, t.name, t.date, "Calculate & Pay Advance Tax if liability > ₹10,000"));

  // 4. INCOME TAX RETURNS (ITR) & ANNUAL FILINGS
  createComplianceEvent(calendar, "ITR Filing (Individuals/Non-Audit)", new Date(2025, 6, 31), "Deadline for ITR-1, 2, 4");
  createComplianceEvent(calendar, "ITR Filing (Audit Cases/Companies)", new Date(2025, 9, 31), "Deadline for Corporate/Audit cases");
  createComplianceEvent(calendar, "GST Annual Return (GSTR-9/9C)", new Date(2025, 11, 31), "Annual reconciliation for FY 2024-25");
}

function createComplianceEvent(cal, title, date, desc) {
  const event = cal.createAllDayEvent("📌 COMPLIANCE: " + title, date, { description: desc });
  event.addEmailReminder(1440); // 1 day before
  event.addPopupReminder(60);   // 1 hour before
}
