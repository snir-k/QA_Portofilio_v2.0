/* global Chart, XLSX, html2pdf, html2canvas */

// משתנים גלובליים לשמירת מופעי הגרפים לצורך עדכון ורענון דינמי
let statusPieChartInstance = null;
let durationBarChartInstance = null;

document.addEventListener('DOMContentLoaded', () => {
    console.log("בלש השכבות: Frontend UI Layer fully initialized.");

    initLogAccordion();
    initActionButtons();
    initJiraSearch();
    initAdminCMSModal()
    initCarouselNavigation();

    // צביעה דינמית וניהול Fallback אקטיבי לתמונות שבורות
    applyCarouselColors();

    if (typeof Chart !== 'undefined') {
        fetchInitialDataForCharts();
    } else {
        setTimeout(fetchInitialDataForCharts, 500);
    }
});

/**
 * מנגנון לפתיחה וסגירה דינמית של שורות הלוג בטבלה
 */
function initLogAccordion() {
    const testRows = document.querySelectorAll('.test-row.status-failed');
    testRows.forEach(row => {
        row.style.cursor = 'pointer';
        row.addEventListener('click', () => {
            const testId = row.getAttribute('data-id');
            const logRow = document.querySelector(`.log-row[data-for="${testId}"]`);
            if (logRow) {
                const isDisplayed = logRow.style.display === 'table-row';
                logRow.style.display = isDisplayed ? 'none' : 'table-row';
                if (isDisplayed) {
                    row.classList.remove('active-log-parent');
                } else {
                    row.classList.add('active-log-parent');
                }
            }
        });
    });
}

/**
 * שליפת הנתונים המלאה בטעינה ראשונית כדי לאכלס את הגרפים
 */
function fetchInitialDataForCharts() {
    fetch('/api/tests')
        .then(res => res.json())
        .then(data => updateCharts(data))
        .catch(err => console.error("Error loading initial chart data:", err));
}

/**
 * פונקציה מרכזית לציור ועדכון הגרפים (Chart.js) על סמך מערך נתונים
 */
function updateCharts(testArray) {
    if (testArray.length === 0) {
        if (statusPieChartInstance) statusPieChartInstance.destroy();
        if (durationBarChartInstance) durationBarChartInstance.destroy();
        return;
    }
    const passedCount = testArray.filter(t => t.status === 'Passed').length;
    const failedCount = testArray.filter(t => t.status === 'Failed').length;
    const labels = testArray.map(t => t.id);
    const durations = testArray.map(t => t.execution_time);

    if (statusPieChartInstance) statusPieChartInstance.destroy();
    const ctxPie = document.getElementById('statusPieChart').getContext('2d');
    statusPieChartInstance = new Chart(ctxPie, {
        type: 'pie',
        data: {
            labels: ['Passed', 'Failed'],
            datasets: [{ data: [passedCount, failedCount], backgroundColor: ['#36b37e', '#ff5630'], borderWidth: 1, borderColor: '#2d2d44' }]
        },
        options: { responsive: true, plugins: { legend: { position: 'bottom', labels: { color: '#a5adba' } } } }
    });

    if (durationBarChartInstance) durationBarChartInstance.destroy();
    const ctxBar = document.getElementById('durationBarChart').getContext('2d');
    durationBarChartInstance = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{ label: 'זמן ריצה (בשניות)', data: durations, backgroundColor: '#0052cc', borderRadius: 4 }]
        },
        options: {
            responsive: true,
            plugins: { legend: { display: false } },
            scales: { x: { ticks: { color: '#a5adba' }, grid: { display: false } }, y: { ticks: { color: '#a5adba' }, grid: { color: '#444' } } }
        }
    });
}

/**
 * מנגנון חיפוש חכם מול השרת בפייתון
 */
function initJiraSearch() {
    const searchCategory = document.getElementById('searchCategory');
    const searchInput = document.getElementById('searchInput');
    const tableBody = document.getElementById('testTableBody');

    if (!searchCategory || !searchInput || !tableBody) return;

    searchInput.addEventListener('input', () => {
        const category = searchCategory.value;
        const query = searchInput.value;

        fetch('/api/tests/search?category=' + category + '&query=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                tableBody.innerHTML = '';
                if (data.length === 0) {
                    tableBody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 20px; color: #a5adba;">לא נמצאו תוצאות מתאימות לחיפוש.</td></tr>`;
                    updateCharts([]);
                    return;
                }
                data.forEach(test => {
                    const row = document.createElement('tr');
                    const statusClass = test.status ? test.status.toLowerCase() : 'unknown';
                    row.className = `test-row status-${statusClass}`;
                    row.setAttribute('data-id', test.id);

                    row.innerHTML = `
                        <td><strong>${test.id}</strong></td>
                        <td>${test.name}</td>
                        <td><span class="badge badge-type">${test.type}</span></td>
                        <td><span class="badge badge-severity">${test.severity}</span></td>
                        <td><span class="status-indicator">${test.status}</span></td>
                        <td>${test.execution_time}s</td>
                        <td>${test.coverage}%</td>
                        <td>${test.stability}%</td>
                    `;
                    tableBody.appendChild(row);

                    if (statusClass === 'failed' && test.log) {
                        const logRow = document.createElement('tr');
                        logRow.className = 'log-row';
                        logRow.setAttribute('data-for', test.id);
                        logRow.innerHTML = `
                            <td colspan="8">
                                <div class="log-trace-box"><strong>Stack Trace Log:</strong><pre>${test.log}</pre></div>
                            </td>
                        `;
                        tableBody.appendChild(logRow);
                    }
                });
                updateCharts(data);
                initLogAccordion();
            })
            .catch(err => console.error("Error during live search sync:", err));
    });
}

/**
 * פונקציה המטפלת בצביעה דינמית וניהול Fallback אקטיבי לתמונות שבורות בצד הלקוח
 */
function applyCarouselColors() {
    const carouselItems = document.querySelectorAll('.carousel-item');

    carouselItems.forEach(item => {
        const color = item.getAttribute('data-color');
        if (color) {
            item.style.borderColor = color;
            item.style.color = color;
        }

        const img = item.querySelector('.tech-uploaded-img');
        if (img) {
            const replaceWithFallback = () => {
                const fallbackSpan = document.createElement('span');
                fallbackSpan.className = 'tech-icon-fallback';
                fallbackSpan.textContent = '🗲';
                item.insertBefore(fallbackSpan, img);
                img.remove();
            };

            if (img.complete && img.naturalWidth === 0) {
                replaceWithFallback();
            } else {
                img.addEventListener('error', replaceWithFallback);
            }
        }
    });
}

/**
 * 🔐 ניהול מודאל סיסמת מנהל לנעילה אוטומטית בכל רענון/יציאה
 */
function initAdminCMSModal() {
    const adminToggleBtn = document.getElementById('adminToggleBtn');
    const adminModal = document.getElementById('adminModal');
    const closeAuthBtn = document.getElementById('closeAuthBtn');
    const submitAuthBtn = document.getElementById('submitAuthBtn');
    const adminPasswordInput = document.getElementById('adminPassword');
    const togglePasswordBtn = document.getElementById('togglePasswordBtn');
    const authErrorMessage = document.getElementById('authErrorMessage');
    const cmsPanel = document.getElementById('cmsPanel');

    if (!adminToggleBtn || !adminModal || !closeAuthBtn || !submitAuthBtn || !adminPasswordInput || !togglePasswordBtn || !cmsPanel) return;

    let isAdminAuthenticated = false;

    adminToggleBtn.addEventListener('click', () => {
        if (!isAdminAuthenticated) {
            adminModal.style.display = 'flex';
            adminPasswordInput.value = '';
            authErrorMessage.style.display = 'none';
            adminPasswordInput.focus();
        } else {
            isAdminAuthenticated = false;
            cmsPanel.style.display = 'none';
            adminToggleBtn.className = 'btn btn-dark';
            adminToggleBtn.textContent = 'מצב מנהל: OFF 🔴 (לחץ להתחברות)';
        }
    });

    closeAuthBtn.addEventListener('click', () => {
        adminModal.style.display = 'none';
    });

    togglePasswordBtn.addEventListener('click', () => {
        const isPassword = adminPasswordInput.type === 'password';
        adminPasswordInput.type = isPassword ? 'text' : 'password';
        togglePasswordBtn.textContent = isPassword ? '🙈' : '👁️';
    });

    submitAuthBtn.addEventListener('click', () => {
        if (adminPasswordInput.value === 'admin123') {
            isAdminAuthenticated = true;
            adminModal.style.display = 'none';
            cmsPanel.style.display = 'block';
            adminToggleBtn.className = 'btn btn-success';
            adminToggleBtn.textContent = 'מצב מנהל: ON 🟢 (לחץ לנעילה)';
        } else {
            authErrorMessage.style.display = 'block';
            adminPasswordInput.value = '';
            adminPasswordInput.focus();
        }
    });

    adminPasswordInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            submitAuthBtn.click();
        }
    });
}

/**
 * מנגנון לניהול קרוסלת הטכנולוגיות בעזרת לחצני ניווט אובסדיאן
 */
function initCarouselNavigation() {
    const prevBtn = document.getElementById('prevTechBtn');
    const nextBtn = document.getElementById('nextTechBtn');
    const track = document.getElementById('carouselTrack');

    if (!prevBtn || !nextBtn || !track) return;

    let currentTranslate = 0;
    const step = 180;

    prevBtn.addEventListener('click', () => {
        currentTranslate += step;
        if (currentTranslate > 0) currentTranslate = 0;
        track.style.transform = `translateX(${currentTranslate}px)`;
    });

    nextBtn.addEventListener('click', () => {
        const maxScroll = -(track.scrollWidth - track.parentElement.clientWidth);
        currentTranslate -= step;
        if (currentTranslate < maxScroll) currentTranslate = maxScroll;
        track.style.transform = `translateX(${currentTranslate}px)`;
    });
}

/**
 * 🛠️ ריכוז פיתוח מאזיני לחיצה עבור 4 כפתורי הפעולה והאוטומציה המורחבים
 */
function initActionButtons() {
    const excelBtn = document.getElementById('exportExcelBtn');
    const pdfBtn = document.getElementById('exportPdfBtn');
    const snapshotBtn = document.getElementById('snapshotBtn');
    const runBtn = document.getElementById('runSimulationBtn');

    // 📊 1. מנגנון ייצוא ל-Excel עם תמיכת RTL מלאה
    if (excelBtn) {
        excelBtn.addEventListener('click', () => {
            console.log("Excel Export triggered via API data Fetch.");
            fetch('/api/tests')
                .then(res => res.json())
                .then(testsData => {
                    const formattedRows = testsData.map(test => ({
                        id: test.id,
                        name: test.name,
                        type: test.type,
                        severity: test.severity,
                        status: test.status,
                        duration: test.execution_time,
                        coverage: test.coverage,
                        stability: test.stability
                    }));
                    const wb = XLSX.utils.book_new();
                    const ws = XLSX.utils.json_to_sheet(formattedRows, { skipHeader: true });
                    const headers = ["מזהה בדיקה", "שם הבדיקה", "סוג", "חומרה", "סטטוס", "זמן ריצה", "כיסוי קוד", "מדד יציבות"];
                    XLSX.utils.sheet_add_aoa(ws, [headers], { origin: "A1" });
                    if (!ws['!views']) ws['!views'] = [];
                    ws['!views'].push({ RTL: true });
                    XLSX.utils.book_append_sheet(wb, ws, "דוח בדיקות אוטומציה");
                    XLSX.writeFile(wb, "Automation_Dashboard_Report.xlsx");
                })
                .catch(err => console.error("Error generating Excel report:", err));
        });
    }

    // 📄 2. מנגנון הפקת דוח PDF רוחבי, קריא ונגיש דרך שיבוט מוגן
    if (pdfBtn) {
        pdfBtn.addEventListener('click', () => {
            console.log("PDF Report generation triggered.");
            const originalTable = document.getElementById('testTable');
            if (!originalTable) return;

            const clonedTable = originalTable.cloneNode(true);
            const headers = clonedTable.querySelectorAll('thead th');
            const cleanHeaders = ["מזהה בדיקה", "שם הבדיקה", "סוג", "חומרה", "סטטוס", "זמן ריצה", "כיסוי קוד", "מדד יציבות"];
            headers.forEach((th, index) => {
                if (cleanHeaders[index]) th.textContent = cleanHeaders[index];
            });

            clonedTable.style.backgroundColor = '#ffffff';
            clonedTable.style.color = '#000000';
            clonedTable.style.width = '100%';

            clonedTable.querySelectorAll('th').forEach(th => {
                th.style.backgroundColor = '#f4f5f7';
                th.style.color = '#172b4d';
                th.style.borderBottom = '2px solid #c1c7d0';
                th.style.textAlign = 'right';
                th.style.padding = '10px';
            });
            clonedTable.querySelectorAll('td').forEach(td => {
                td.style.color = '#000000';
                td.style.borderBottom = '1px solid #dfe1e6';
                td.style.padding = '10px';
                td.style.textAlign = 'right';
            });
            clonedTable.querySelectorAll('strong').forEach(str => { str.style.color = '#000000'; });
            clonedTable.querySelectorAll('.log-row').forEach(log => { log.remove(); });

            const opt = {
                margin:       12,
                filename:     'Automation_Dashboard_Report.pdf',
                image:        { type: 'jpeg', quality: 0.98 },
                html2canvas:  { scale: 2, useCORS: true, logging: false, background: '#ffffff' },
                jsPDF:        { unit: 'mm', format: 'a4', orientation: 'landscape' }
            };

            html2pdf().set(opt).from(clonedTable).save()
                .catch(err => console.error("Error during PDF compilation:", err));
        });
    }

    // 📸 3. מנגנון צילום מסך Snapshot של אלמנט הטבלה בלבד לתוך קובץ PNG
    if (snapshotBtn) {
        snapshotBtn.addEventListener('click', () => {
            console.log("Snapshot capture triggered.");
            const targetElement = document.getElementById('testTable');
            if (!targetElement) return;

            const options = { scale: 2, useCORS: true, logging: false, backgroundColor: null };

            html2canvas(targetElement, options)
                .then(canvas => {
                    const imgData = canvas.toDataURL('image/png');
                    const downloadLink = document.createElement('a');
                    downloadLink.href = imgData;
                    downloadLink.download = 'Automation_Table_Snapshot.png';
                    document.body.appendChild(downloadLink);
                    downloadLink.click();
                    document.body.removeChild(downloadLink);
                })
                .catch(err => console.error("Error during snapshot compilation:", err));
        });
    }

    // 🔄 4. מנגנון הרצת סימולציית הבדיקות הדינמית בלייב עם Spinner מבוסס שרת
    if (runBtn) {
        runBtn.addEventListener('click', () => {
            console.log("Automation simulation suite triggered.");

            // הגנה מכפל לחיצות: מניעת הרצה נוספת כל עוד הסימולציה פעילה
            if (runBtn.classList.contains('btn-loading')) return;

            // 1. שמירת הטקסט המקורי והפעלת אפקט Spinner הטעינה הויזואלי
            const originalText = runBtn.innerHTML;
            runBtn.classList.add('btn-loading');
            runBtn.innerHTML = 'מריץ טסטים בלייב... <span class="spinner-icon">⏳</span>';

            // 2. שליחת בקשת POST רשמית ל-API של שרת הפייתון
            fetch('/api/simulation/run', { method: 'POST' })
                .then(res => {
                    if (!res.ok) throw new Error('Simulation failed on server.');
                    return res.json();
                })
                .then(response => {
                    // 3. עדכון דינמי של הטבלה והגרפים בלייב ללא רענון עמוד!
                    const tableBody = document.getElementById('testTableBody');
                    if (tableBody && response.tests) {
                        // ה-Jira-like Search שלנו כבר יודע לקבל מערך נתונים ולרנדר מחדש.
                        // פשוט נפעיל אירוע קלט ריק על החיפוש כדי שימשוך את הנתונים החדשים,
                        // או שנרנדר את מערך הנתונים ישירות לגרפים
                        updateCharts(response.tests);

                        // ניתוח הרצה מהיר: נדמה רענון קל של תיבת החיפוש לעדכון השורות בטבלה
                        const searchInput = document.getElementById('searchInput');
                        if (searchInput) {
                            searchInput.dispatchEvent(new Event('input'));
                        }
                    }
                    console.log("Simulation finished successfully.");
                })
                .catch(err => console.error("Error running automation simulation:", err))
                .finally(() => {
                    // 4. הסרת אפקט הטעינה והחזרת הכפתור למצבו הרגיל והיוקרתי
                    runBtn.classList.remove('btn-loading');
                    runBtn.innerHTML = originalText;
                });
        });
    }

}
