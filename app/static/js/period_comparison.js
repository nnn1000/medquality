document.addEventListener('DOMContentLoaded', function() {
    // 初始化图表
    const chart = echarts.init(document.getElementById('chart-container'));
    
    // 设置默认日期范围（当前月份）
    const today = new Date();
    const firstDay = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDay = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    document.getElementById('start-date').value = firstDay.toISOString().split('T')[0];
    document.getElementById('end-date').value = lastDay.toISOString().split('T')[0];
    
    // 查询按钮点击事件
    document.getElementById('query-btn').addEventListener('click', function() {
        const indicatorCode = document.getElementById('indicator-select').value;
        const startDate = document.getElementById('start-date').value;
        const endDate = document.getElementById('end-date').value;
        
        if (!indicatorCode) {
            alert('请选择指标');
            return;
        }
        
        if (!startDate || !endDate) {
            alert('请选择日期范围');
            return;
        }
        
        // 发送请求获取数据
        fetch(`/api/statistics/period_comparison?indicator_code=${indicatorCode}&start_date=${startDate}&end_date=${endDate}`)
            .then(response => response.json())
            .then(data => {
                updateChart(data);
                updateTable(data);
            })
            .catch(error => {
                console.error('Error:', error);
                alert('获取数据失败');
            });
    });
    
    // 更新图表
    function updateChart(data) {
        const currentDates = data.current_period.map(item => item.date);
        const currentValues = data.current_period.map(item => item.value);
        const lastYearValues = data.last_year.map(item => item.value);
        
        const option = {
            title: {
                text: '同期对比分析',
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    type: 'shadow'
                }
            },
            legend: {
                data: ['当前值', '去年同期值'],
                top: 30
            },
            grid: {
                left: '3%',
                right: '4%',
                bottom: '3%',
                containLabel: true
            },
            xAxis: {
                type: 'category',
                data: currentDates,
                axisLabel: {
                    rotate: 45
                }
            },
            yAxis: {
                type: 'value'
            },
            series: [
                {
                    name: '当前值',
                    type: 'bar',
                    data: currentValues
                },
                {
                    name: '去年同期值',
                    type: 'bar',
                    data: lastYearValues
                }
            ]
        };
        
        chart.setOption(option);
    }
    
    // 更新表格
    function updateTable(data) {
        const tbody = document.querySelector('#comparison-table tbody');
        tbody.innerHTML = '';
        
        data.current_period.forEach((current, index) => {
            const lastYear = data.last_year[index];
            const change = lastYear && current.value ? 
                ((current.value - lastYear.value) / lastYear.value * 100).toFixed(2) + '%' : 
                'N/A';
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${current.date}</td>
                <td>${current.value !== null ? current.value.toFixed(2) : 'N/A'}</td>
                <td>${lastYear && lastYear.value !== null ? lastYear.value.toFixed(2) : 'N/A'}</td>
                <td>${change}</td>
            `;
            tbody.appendChild(row);
        });
    }
    
    // 窗口大小改变时重绘图表
    window.addEventListener('resize', function() {
        chart.resize();
    });
}); 