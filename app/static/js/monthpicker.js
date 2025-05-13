/**
 * 月度选择器 - 自定义月度选择组件
 * 用于报告周期选择，允许用户选择开始月份和结束月份，支持跨年度选择
 */
$(document).ready(function() {
    // 初始化月度选择器
    initializeMonthPicker();
});

function initializeMonthPicker() {
    // 查找所有具有 data-monthpicker 属性的元素
    $('[data-monthpicker]').each(function() {
        const input = $(this);
        const container = $('<div class="monthpicker-container position-relative"></div>');
        
        // 创建显示框
        const display = $('<div class="monthpicker-display form-control d-flex justify-content-between align-items-center cursor-pointer"></div>');
        const displayText = $('<span></span>');
        const icon = $('<i class="fas fa-calendar-alt"></i>');
        
        display.append(displayText);
        display.append(icon);
        
        // 创建下拉面板
        const dropdown = $('<div class="monthpicker-dropdown card shadow position-absolute w-100 d-none" style="z-index: 1000;"></div>');
        const dropdownContent = $('<div class="card-body p-2"></div>');
        
        // 添加年份选项 (从2020年到当前年份后2年)
        const currentYear = new Date().getFullYear();
        const years = [];
        for(let year = 2020; year <= currentYear + 2; year++) {
            years.push(year);
        }
        
        // 年份选择器 - 单个下拉框控制整个报告周期的年份
        const yearSelector = $('<div class="mb-3"></div>');
        const yearLabel = $('<label class="form-label">报告周期</label>');
        yearSelector.append(yearLabel);
        
        // 年份选择器
        const yearSelect = $('<select class="form-select form-select-sm picker-year mb-2"></select>');
        for(const year of years) {
            yearSelect.append(`<option value="${year}">${year}年</option>`);
        }
        yearSelect.val(currentYear); // 默认当前年份
        
        // 所有月份选择器
        const monthButtons = $('<div class="d-flex flex-wrap gap-1 mb-3"></div>');
        
        // 添加所有月份按钮 (1-12月)
        for(let month = 1; month <= 12; month++) {
            const monthButton = $(`<button type="button" data-month="${month}" class="btn btn-sm btn-outline-primary picker-month">${month}月</button>`);
            monthButtons.append(monthButton);
        }
        
        yearSelector.append(yearSelect);
        yearSelector.append(monthButtons);
        
        // 结束日期选择部分
        const endDateSelector = $('<div class="mb-3"></div>');
        const endDateLabel = $('<label class="form-label">结束日期</label>');
        endDateSelector.append(endDateLabel);
        
        // 结束年份选择器
        const endYearSelect = $('<select class="form-select form-select-sm monthpicker-end-year mb-2"></select>');
        for(const year of years) {
            endYearSelect.append(`<option value="${year}">${year}年</option>`);
        }
        endYearSelect.val(currentYear); // 默认当前年份
        endDateSelector.append(endYearSelect);
        
        // 结束月份选择器
        const endMonthButtons = $('<div class="d-flex flex-wrap gap-1"></div>');
        
        // 添加结束月份按钮
        for(let month = 1; month <= 12; month++) {
            const monthButton = $(`<button type="button" data-month="${month}" class="btn btn-sm btn-outline-primary monthpicker-end-month">${month}月</button>`);
            endMonthButtons.append(monthButton);
        }
        endDateSelector.append(endMonthButtons);
        
        // 确认按钮
        const confirmRangeButton = $('<button type="button" class="btn btn-primary w-100 mt-3">确认选择</button>');
        
        // 将所有元素组合起来
        dropdownContent.append(yearSelector);
        dropdownContent.append(endDateSelector);
        dropdownContent.append(confirmRangeButton);
        dropdown.append(dropdownContent);
        
        // 替换原始输入
        input.hide();
        input.after(container);
        container.append(input);
        container.append(display);
        container.append(dropdown);
        
        // 设置初始值
        updateDisplayFromInput(input, displayText);
        
        // 添加事件监听
        display.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            dropdown.toggleClass('d-none');
            
            // 根据输入值更新年份选择
            const inputVal = input.val();
            if (inputVal) {
                // 尝试解析日期范围格式 "2023年1月-3月" 或 "2023年1月-2024年3月"
                const rangeMatch = inputVal.match(/^(\d{4})年(\d{1,2})月-(\d{4})年(\d{1,2})月$/);
                const singleYearMatch = inputVal.match(/^(\d{4})年(\d{1,2})月-(\d{1,2})月$/);
                
                if (rangeMatch) {
                    // 跨年日期范围
                    const startYear = rangeMatch[1];
                    const startMonth = rangeMatch[2];
                    const endYear = rangeMatch[3];
                    const endMonth = rangeMatch[4];
                    
                    yearSelect.val(startYear);
                    endYearSelect.val(endYear);
                    
                    monthButtons.find('.picker-month').removeClass('active');
                    monthButtons.find(`[data-month="${startMonth}"]`).addClass('active');
                    
                    endMonthButtons.find('.monthpicker-end-month').removeClass('active');
                    endMonthButtons.find(`[data-month="${endMonth}"]`).addClass('active');
                } else if (singleYearMatch) {
                    // 单年日期范围
                    const year = singleYearMatch[1];
                    const startMonth = singleYearMatch[2];
                    const endMonth = singleYearMatch[3];
                    
                    yearSelect.val(year);
                    endYearSelect.val(year);
                    
                    monthButtons.find('.picker-month').removeClass('active');
                    monthButtons.find(`[data-month="${startMonth}"]`).addClass('active');
                    
                    endMonthButtons.find('.monthpicker-end-month').removeClass('active');
                    endMonthButtons.find(`[data-month="${endMonth}"]`).addClass('active');
                } else {
                    // 默认当前年
                    yearSelect.val(currentYear);
                    endYearSelect.val(currentYear);
                }
            } else {
                yearSelect.val(currentYear);
                endYearSelect.val(currentYear);
            }
        });
        
        // 点击年份下拉框不隐藏面板
        yearSelect.on('click', function(e) {
            e.stopPropagation();
        });
        
        endYearSelect.on('click', function(e) {
            e.stopPropagation();
        });
        
        // 选择开始月份
        monthButtons.find('.picker-month').on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            monthButtons.find('.picker-month').removeClass('active');
            $(this).addClass('active');
            
            // 自动将结束年份设置为与开始年份相同
            endYearSelect.val(yearSelect.val());
        });
        
        // 选择结束月份
        endMonthButtons.find('.monthpicker-end-month').on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            endMonthButtons.find('.monthpicker-end-month').removeClass('active');
            $(this).addClass('active');
        });
        
        // 确认日期范围选择
        confirmRangeButton.on('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const startYear = yearSelect.val();
            const endYear = endYearSelect.val();
            const activeStartMonthButton = monthButtons.find('.active');
            const activeEndMonthButton = endMonthButtons.find('.active');
            
            if (activeStartMonthButton.length && activeEndMonthButton.length) {
                const startMonth = activeStartMonthButton.data('month');
                const endMonth = activeEndMonthButton.data('month');
                
                // 验证日期范围有效性
                if (startYear > endYear || (startYear === endYear && startMonth > endMonth)) {
                    alert('开始日期不能晚于结束日期');
                    return;
                }
                
                // 标准化日期范围格式
                let value = standardizePeriodFormat(startYear, startMonth, endYear, endMonth);
                
                input.val(value);
                displayText.text(value);
                dropdown.addClass('d-none');
                
                // 立即更新隐藏字段，不使用setTimeout
                updateHiddenPeriodField(value);
                
                // 触发change事件
                input.trigger('change');
                console.log('monthpicker: 触发了change事件，当前值:', value);
            } else {
                alert('请选择开始月份和结束月份');
            }
        });
        
        // 更新隐藏字段的函数
        function updateHiddenPeriodField(value) {
            console.log('更新隐藏字段，当前值:', value);
            const hiddenField = $('#period_id_hidden');
            if (hiddenField.length) {
                // 查找与选择的周期名称匹配的ID
                try {
                    const periodData = JSON.parse($('#period-data').text());
                    let foundPeriod = null;
                    
                    // 尝试直接匹配
                    for (let i = 0; i < periodData.length; i++) {
                        if (periodData[i].name === value) {
                            foundPeriod = periodData[i];
                            break;
                        }
                    }
                    
                    // 如果找到匹配的周期，更新隐藏字段
                    if (foundPeriod) {
                        hiddenField.val(foundPeriod.id);
                        console.log('找到匹配的周期ID:', foundPeriod.id);
                    } else {
                        // 如果没有匹配，尝试寻找最佳匹配
                        console.log('未找到精确匹配，尝试寻找最佳匹配');
                        let match = findClosestPeriod(value, periodData);
                        if (match) {
                            hiddenField.val(match.id);
                            console.log('找到最佳匹配的周期ID:', match.id);
                        } else if (periodData.length > 0) {
                            // 如果没有最佳匹配，使用第一个可用的周期
                            hiddenField.val(periodData[0].id);
                            console.log('使用默认周期ID:', periodData[0].id);
                        }
                    }
                } catch (e) {
                    console.error('解析周期数据失败:', e);
                }
            }
        }
        
        // 查找最接近的周期
        function findClosestPeriod(value, periodData) {
            // 解析日期范围值
            const rangeMatch = value.match(/^(\d{4})年(\d{1,2})月-(\d{1,2})月$/);
            const crossYearMatch = value.match(/^(\d{4})年(\d{1,2})月-(\d{4})年(\d{1,2})月$/);
            const quarterMatch = value.match(/^(\d{4})年第(\d)季度$/);
            
            if (rangeMatch) {
                const year = parseInt(rangeMatch[1]);
                const startMonth = parseInt(rangeMatch[2]);
                const endMonth = parseInt(rangeMatch[3]);
                
                // 查找季度匹配
                if (startMonth === 1 && endMonth === 3) {
                    return findPeriodByNamePattern(periodData, `${year}年第1季度`);
                } else if (startMonth === 4 && endMonth === 6) {
                    return findPeriodByNamePattern(periodData, `${year}年第2季度`);
                } else if (startMonth === 7 && endMonth === 9) {
                    return findPeriodByNamePattern(periodData, `${year}年第3季度`);
                } else if (startMonth === 10 && endMonth === 12) {
                    return findPeriodByNamePattern(periodData, `${year}年第4季度`);
                }
            } else if (quarterMatch) {
                const year = parseInt(quarterMatch[1]);
                const quarter = parseInt(quarterMatch[2]);
                
                // 将季度转换为月份范围
                let startMonth, endMonth;
                switch(quarter) {
                    case 1: startMonth = 1; endMonth = 3; break;
                    case 2: startMonth = 4; endMonth = 6; break;
                    case 3: startMonth = 7; endMonth = 9; break;
                    case 4: startMonth = 10; endMonth = 12; break;
                }
                
                return findPeriodByNamePattern(periodData, `${year}年${startMonth}月-${endMonth}月`);
            }
            
            return null;
        }
        
        // 按名称模式查找周期
        function findPeriodByNamePattern(periodData, pattern) {
            for (let i = 0; i < periodData.length; i++) {
                if (periodData[i].name.includes(pattern)) {
                    return periodData[i];
                }
            }
            return null;
        }
        
        // 标准化报告周期格式
        function standardizePeriodFormat(startYear, startMonth, endYear, endMonth) {
            // 将数字转换为整数
            startYear = parseInt(startYear);
            startMonth = parseInt(startMonth);
            endYear = parseInt(endYear);
            endMonth = parseInt(endMonth);
            
            // 季度判断
            if (startYear === endYear) {
                // 第一季度: 1-3月
                if (startMonth === 1 && endMonth === 3) {
                    return `${startYear}年第1季度`;
                }
                // 第二季度: 4-6月
                else if (startMonth === 4 && endMonth === 6) {
                    return `${startYear}年第2季度`;
                }
                // 第三季度: 7-9月
                else if (startMonth === 7 && endMonth === 9) {
                    return `${startYear}年第3季度`;
                }
                // 第四季度: 10-12月
                else if (startMonth === 10 && endMonth === 12) {
                    return `${startYear}年第4季度`;
                }
                // 上半年: 1-6月
                else if (startMonth === 1 && endMonth === 6) {
                    return `${startYear}年上半年`;
                }
                // 下半年: 7-12月
                else if (startMonth === 7 && endMonth === 12) {
                    return `${startYear}年下半年`;
                }
                // 全年: 1-12月
                else if (startMonth === 1 && endMonth === 12) {
                    return `${startYear}年`;
                }
                // 单月
                else if (startMonth === endMonth) {
                    return `${startYear}年${startMonth}月`;
                }
                // 其他同年份范围
                else {
                    return `${startYear}年${startMonth}月-${endMonth}月`;
                }
            } else {
                // 跨年份范围
                return `${startYear}年${startMonth}月-${endYear}年${endMonth}月`;
            }
        }
        
        // 年份变更事件
        yearSelect.on('change', function() {
            // 当开始年份变更时，可以选择同步更新结束年份
            const startYear = yearSelect.val();
            endYearSelect.val(startYear);
        });
        
        // 点击其他地方时关闭面板
        $(document).on('click', function(e) {
            if (!$(e.target).closest('.monthpicker-container').length) {
                dropdown.addClass('d-none');
            }
        });
    });
}

// 从输入值更新显示文本
function updateDisplayFromInput(input, displayText) {
    const value = input.val();
    if (value) {
        displayText.text(value);
    } else {
        displayText.text('请选择报告周期');
    }
} 