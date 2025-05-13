// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', function() {
    // 初始化提示框
    initializeTooltips();
    
    // 自动关闭警告框
    initializeAlertDismiss();
    
    // 处理表单依赖关系
    initializeFormDependencies();
    
    // 初始化图表（如果页面上有图表容器）
    initializeCharts();
});

// 初始化 Bootstrap 提示框
function initializeTooltips() {
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
}

// 自动关闭警告框
function initializeAlertDismiss() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert && alert.parentNode) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    });
}

// 处理表单字段依赖关系
function initializeFormDependencies() {
    // 处理报告周期类型选择
    const periodTypeSelect = document.querySelector('#period_type');
    if (periodTypeSelect) {
        const quarterField = document.querySelector('#quarter').closest('.mb-3');
        const monthField = document.querySelector('#month').closest('.mb-3');
        
        // 初始化基于当前选择的状态
        updatePeriodFields(periodTypeSelect.value, quarterField, monthField);
        
        // 添加更改事件监听器
        periodTypeSelect.addEventListener('change', function() {
            updatePeriodFields(this.value, quarterField, monthField);
        });
    }
    
    // 处理指标信息显示
    const indicatorSelect = document.querySelector('#indicator_id');
    if (indicatorSelect) {
        indicatorSelect.addEventListener('change', function() {
            updateIndicatorInfo(this.value);
        });
        
        // 如果已经有选择，初始化显示
        if (indicatorSelect.value) {
            updateIndicatorInfo(indicatorSelect.value);
        }
    }
}

// 更新周期字段显示状态
function updatePeriodFields(periodType, quarterField, monthField) {
    if (periodType === 'year') {
        quarterField.style.display = 'none';
        monthField.style.display = 'none';
    } else if (periodType === 'quarter') {
        quarterField.style.display = 'block';
        monthField.style.display = 'none';
    } else if (periodType === 'month') {
        quarterField.style.display = 'none';
        monthField.style.display = 'block';
    }
}

// 更新指标信息显示
function updateIndicatorInfo(indicatorId) {
    const infoContainer = document.querySelector('#indicator-info');
    if (!infoContainer || !indicatorId) return;
    
    // 这里假设有一个API端点返回指标信息
    fetch(`/api/indicators/${indicatorId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                let html = `
                    <div class="alert alert-info">
                        <h6>指标定义：</h6>
                        <p>${data.indicator.definition || '无'}</p>
                        <h6>分子说明：</h6>
                        <p>${data.indicator.numerator_description || '无'}</p>
                        <h6>分母说明：</h6>
                        <p>${data.indicator.denominator_description || '无'}</p>
                    </div>
                `;
                infoContainer.innerHTML = html;
            }
        })
        .catch(error => {
            console.error('获取指标信息失败', error);
        });
}

// 初始化图表
function initializeCharts() {
    // 检查页面上是否有图表容器
    const categoryChartContainer = document.getElementById('category-distribution-chart');
    if (categoryChartContainer) {
        renderCategoryChart(categoryChartContainer);
    }
    
    const achievementChartContainer = document.getElementById('achievement-rate-chart');
    if (achievementChartContainer) {
        renderAchievementChart(achievementChartContainer);
    }
}

// 渲染指标类别分布图表
function renderCategoryChart(container) {
    // 获取数据（通常从容器的data属性或全局变量）
    const categoryNames = JSON.parse(container.dataset.names || '[]');
    const categoryCounts = JSON.parse(container.dataset.counts || '[]');
    
    // 这里可以使用Chart.js或其他图表库绘制图表
    // 示例代码使用Chart.js（需要在页面中引入）
    if (typeof Chart !== 'undefined' && categoryNames.length > 0) {
        new Chart(container, {
            type: 'doughnut',
            data: {
                labels: categoryNames,
                datasets: [{
                    data: categoryCounts,
                    backgroundColor: [
                        '#4e73df', '#1cc88a', '#36b9cc', '#f6c23e'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    position: 'bottom'
                }
            }
        });
    }
}

// 渲染达标率图表
function renderAchievementChart(container) {
    // 获取达标率数据
    const achievementRate = parseFloat(container.dataset.rate || '0');
    
    // 使用Chart.js绘制仪表盘图表
    if (typeof Chart !== 'undefined') {
        new Chart(container, {
            type: 'doughnut',
            data: {
                labels: ['达标', '未达标'],
                datasets: [{
                    data: [achievementRate, 100 - achievementRate],
                    backgroundColor: ['#1cc88a', '#e74a3b']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutoutPercentage: 80,
                legend: {
                    display: false
                },
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem, data) {
                            return data.labels[tooltipItem.index] + ': ' + 
                                data.datasets[0].data[tooltipItem.index] + '%';
                        }
                    }
                }
            }
        });
        
        // 在中间显示达标率
        const ctx = container.getContext('2d');
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.font = 'bold 30px Arial';
        ctx.fillStyle = '#444';
        ctx.fillText(achievementRate + '%', container.width / 2, container.height / 2);
    }
} 