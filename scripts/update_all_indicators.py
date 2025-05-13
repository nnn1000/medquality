#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.indicator import Indicator, IndicatorCategory

# 创建应用上下文
app = create_app()
app.app_context().push()

def update_all_indicators():
    """更新所有指标信息"""
    
    print("开始更新所有指标信息...")
    
    # 获取指标类别ID
    category_ids = {}
    categories = {
        'A': '急诊和日间医疗质量',
        'B': '医疗行为质量',
        'C': '结果质量',
        'D': '病历质量'
    }
    
    for code, name in categories.items():
        category = IndicatorCategory.query.filter_by(name=name).first()
        if category:
            category_ids[code] = category.id
        else:
            category = IndicatorCategory(name=name, description=f"包含{name}相关的指标")
            db.session.add(category)
            db.session.flush()
            category_ids[code] = category.id
    
    # 提交类别更改
    db.session.commit()
    
    # 定义所有指标
    indicators = [
        # A类指标
        {
            'code': 'A01',
            'name': '平均急救响应时间',
            'numerator_description': '急救响应时间总时长',
            'denominator_description': '车次',
            'category_id': category_ids['A']
        },
        {
            'code': 'A02',
            'name': '心脏骤停复苏成功率',
            'numerator_description': '心脏骤停复苏成功总例次数',
            'denominator_description': '同期心脏骤停患者行心肺复苏术总例次数',
            'category_id': category_ids['A']
        },
        {
            'code': 'A03',
            'name': '急性ST段抬高型心肌梗死再灌注治疗率',
            'numerator_description': '发病12小时内实施再灌注治疗（静脉溶栓和/或PCI）的STEMI患者数',
            'denominator_description': '同期发病12小时内具有再灌注治疗指征的STEMI患者数',
            'category_id': category_ids['A']
        },
        {
            'code': 'A04',
            'name': '急性脑梗死再灌注治疗率',
            'numerator_description': '发病6小时内的急性脑梗死患者给予静脉溶栓治疗和（或）血管内治疗',
            'denominator_description': '发病6小时内的急性脑梗死患者',
            'category_id': category_ids['A']
        },
        {
            'code': 'A05',
            'name': '开展日间医疗服务的医院占比',
            'numerator_description': '开展日间医疗服务的医院数量（如医院开展填写1，否则填写0）',
            'denominator_description': '/',
            'category_id': category_ids['A']
        },
        {
            'code': 'A06',
            'name': '日间手术占择期手术的比例',
            'numerator_description': '日间手术台次数',
            'denominator_description': '同期出院患者择期手术总台次数',
            'category_id': category_ids['A']
        },
        # B类指标
        {
            'code': 'B01',
            'name': '肿瘤治疗前临床TNM分期评估率',
            'numerator_description': '某癌种首次治疗前完成临床TNM分期评估的患者数',
            'denominator_description': '同期首次治疗的某癌种患者数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B02',
            'name': '营养风险筛查率',
            'numerator_description': '完成营养风险筛查住院患者数',
            'denominator_description': '同期住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B03',
            'name': '疼痛评估规范率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['B']
        },
        {
            'code': 'B03.1',
            'name': '门诊疼痛评估规范率',
            'numerator_description': '疼痛门诊疼痛评估例数',
            'denominator_description': '同期门诊患者数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B03.2',
            'name': '住院患者入院8h内评估规范率',
            'numerator_description': '入院8h内完成疼痛程度评估的住院患者例数',
            'denominator_description': '住院患者总例数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B04',
            'name': '门诊处方审核率',
            'numerator_description': '药品收费前药师审核门诊处方张数',
            'denominator_description': '同期门诊总处方张数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B05',
            'name': '急诊处方审核率',
            'numerator_description': '药品收费前药师审核急诊处方张数',
            'denominator_description': '同期急诊处方总处方张数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B06',
            'name': '住院处方审核率',
            'numerator_description': '药品调配前药师审核住院患者用药医嘱条目数',
            'denominator_description': '同期住院患者用药医嘱总条目数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B07',
            'name': '门诊处方审核合格率',
            'numerator_description': '审核合格的门诊处方张数',
            'denominator_description': '同期审核门诊处方总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B08',
            'name': '急诊处方审核合格率',
            'numerator_description': '审核合格的急诊处方张数',
            'denominator_description': '同期审核急诊处方总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B09',
            'name': '基本药物采购品种数占比',
            'numerator_description': '医疗机构采购国家基本药物品种数',
            'denominator_description': '医疗机构同期采购药物品种总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B10',
            'name': '住院处方审核合格率',
            'numerator_description': '药师点评合格的住院患者医嘱条目数',
            'denominator_description': '同期药师点评的总医嘱条目数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B11',
            'name': '住院患者静脉输液规范使用率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['B']
        },
        {
            'code': 'B11.1',
            'name': '住院患者静脉输液使用率',
            'numerator_description': '使用静脉输液的出院患者数',
            'denominator_description': '同期出院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B11.2',
            'name': '住院患者静脉输液平均每床日使用数量',
            'numerator_description': '出院患者使用静脉输液的数量',
            'denominator_description': '同期出院患者实际占用总床日数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B11.3',
            'name': '住院患者静脉输液平均每床日使用体积',
            'numerator_description': '出院患者使用静脉输液的体积',
            'denominator_description': '同期出院患者实际占用总床日数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B11.4',
            'name': '住院患者平均使用输液药品品种数量',
            'numerator_description': '出院患者使用静脉药品品种总数',
            'denominator_description': '同期出院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B12',
            'name': '危急值报告及时率',
            'numerator_description': '危急值通报时间符合规定时间的检验项目数',
            'denominator_description': '同期需要危急值通报的检验项目总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B13',
            'name': '危急值处置及时率',
            'numerator_description': '临床医生在符合规定时间处置的危急值项目数',
            'denominator_description': '同期需要处置的危急值检验项目数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B14',
            'name': '室间质评项目合格率',
            'numerator_description': '室间质评合格的检验项目数',
            'denominator_description': '同期参加室间质评检验项目总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15',
            'name': '早期康复介入率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.1',
            'name': '早期康复介入率（神经内科）',
            'numerator_description': '接受早期康复介入的重点科室（神经内科）住院患者数',
            'denominator_description': '同期神经内科住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.2',
            'name': '早期康复介入率（神经外科）',
            'numerator_description': '接受早期康复介入的重点科室（神经外科）住院患者数',
            'denominator_description': '同期神经外科住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.3',
            'name': '早期康复介入率（骨科）',
            'numerator_description': '接受早期康复介入的重点科室（骨科）住院患者数',
            'denominator_description': '同期骨科住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.4',
            'name': '早期康复介入率（心血管内科）',
            'numerator_description': '接受早期康复介入的重点科室（心血管内科）住院患者数',
            'denominator_description': '同期心血管内科住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.5',
            'name': '早期康复介入率（重症ICU）',
            'numerator_description': '接受早期康复介入的重点科室（重症ICU）住院患者数',
            'denominator_description': '同期重症ICU住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.6',
            'name': '早期康复介入率（脑卒中）',
            'numerator_description': '接受早期康复介入的脑卒中住院患者数',
            'denominator_description': '同期脑卒中住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.7',
            'name': '早期康复介入率（脊髓损伤）',
            'numerator_description': '接受早期康复介入的脊髓损伤住院患者数',
            'denominator_description': '同期脊髓损伤住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.8',
            'name': '早期康复介入率（髋、膝关节置换术后）',
            'numerator_description': '接受早期康复介入的髋、膝关节置换术后住院患者数',
            'denominator_description': '同期髋、膝关节置换术后住院患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B15.9',
            'name': '康复评定率',
            'numerator_description': '单位时间内接受康复评定的康复医学科住院患者数',
            'denominator_description': '同期康复医学科患者总数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B16',
            'name': '四级手术患者随访率',
            'numerator_description': '住院患者实施四级手术后第一年内完成随访的人数',
            'denominator_description': '同期住院患者实施四级手术总人数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B17',
            'name': '恶性肿瘤患者随访率',
            'numerator_description': '恶性肿瘤患者出院后一年内实施随访的恶性肿瘤患者人数',
            'denominator_description': '同期住院恶性肿瘤人数',
            'category_id': category_ids['B']
        },
        {
            'code': 'B18',
            'name': '每百出院人次主动报告不良事件例次',
            'numerator_description': '主动报告的医疗质量安全不良事件例数',
            'denominator_description': '同期出院患者人次',
            'category_id': category_ids['B']
        },
        {
            'code': 'B19',
            'name': '中医医疗机构中以中医治疗为主的出院患者比例',
            'numerator_description': '年度以中医为主治疗的出院患者人次数',
            'denominator_description': '同期出院患者总人次数',
            'category_id': category_ids['B']
        },
        # C类指标
        {
            'code': 'C01',
            'name': '医院CMI值',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['C']
        },
        {
            'code': 'C02',
            'name': '手术患者住院死亡率',
            'numerator_description': '手术住院死亡人数',
            'denominator_description': '手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C03',
            'name': 'ICU患者病死率',
            'numerator_description': 'ICU 死亡患者数（包括因不可逆疾病而自动出院的患者）',
            'denominator_description': '同期 ICU 收治患者总数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C04',
            'name': '手术并发症发生率',
            'numerator_description': '择期手术患者发生并发症例数',
            'denominator_description': '同期出院的手术患者人数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C05',
            'name': '麻醉并发症发生率',
            'numerator_description': '仅与麻醉及麻醉操作相关的并发症',
            'denominator_description': '单位时间内由麻醉科实施的麻醉例次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C06',
            'name': '非计划重返手术室再手术率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['C']
        },
        {
            'code': 'C06.1',
            'name': '非计划重返手术室再手术率',
            'numerator_description': '手术患者术后非预期重返手术室再次手术例数',
            'denominator_description': '同期手术患者手术例数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C06.2',
            'name': '手术患者术后48小时内非计划重返手术室再次手术率',
            'numerator_description': '手术患者手术后因各种原因导致患者需术后48小时内进行的计划外再次手术例数',
            'denominator_description': '同期出院患者手术例数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C06.3',
            'name': '手术患者术后31天内非计划重返手术室再次手术率',
            'numerator_description': '手术患者手术后因各种原因导致患者需术后31天内进行的计划外再次手术例数',
            'denominator_description': '同期出院患者手术例数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C07',
            'name': '围术期死亡率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['C']
        },
        {
            'code': 'C07.1',
            'name': '手术当日围术期死亡率',
            'numerator_description': '手术当日死亡患者人数',
            'denominator_description': '同期手术患者出院人数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C07.2',
            'name': '术后24小时围术期死亡率',
            'numerator_description': '术后24小时死亡患者人数',
            'denominator_description': '同期手术患者出院人数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C07.3',
            'name': '术后48小时围术期死亡率',
            'numerator_description': '术后48小时死亡患者人数',
            'denominator_description': '同期手术患者出院人数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C08',
            'name': '恶性肿瘤患者生存时间',
            'numerator_description': '综合治疗后生存超过5年以上的某肿瘤患者数',
            'denominator_description': '治疗该肿瘤总患者数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C09',
            'name': '血管内导管相关血流感染发生率',
            'numerator_description': '血管内导管相关血流感染例次数',
            'denominator_description': '同期患者使用血管内导管留置总天数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C10',
            'name': '患者院内压力性损伤发生率',
            'numerator_description': '2期及以上院内压力性损伤发生例数',
            'denominator_description': '同期出院患者人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11',
            'name': '住院患者手术术后获得性指标发生率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.1',
            'name': '手术患者手术后肺栓塞发生率',
            'numerator_description': '手术患者手术后发生肺栓塞发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.2',
            'name': '手术患者手术后深静脉血栓发生率',
            'numerator_description': '手术患者手术后深静脉血栓发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.3',
            'name': '手术患者手术后败血症发生率',
            'numerator_description': '手术患者手术后败血症发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.4',
            'name': '手术患者手术后出血或血肿发生率',
            'numerator_description': '手术患者手术后出血或血肿发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.5',
            'name': '手术患者手术伤口裂开发生率',
            'numerator_description': '手术患者手术后伤口裂开发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.6',
            'name': '手术患者手术后猝死发生率',
            'numerator_description': '手术患者手术后猝死发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.7',
            'name': '手术患者手术后呼吸衰竭发生率',
            'numerator_description': '手术患者手术后呼吸衰竭发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.8',
            'name': '手术患者手术后生理/代谢紊乱发生率',
            'numerator_description': '手术患者手术后生理/代谢紊乱发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.9',
            'name': '与手术/操作相关感染发生例数和发生率',
            'numerator_description': '与手术/操作相关感染发生例数',
            'denominator_description': '同期手术/操作患者总数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.10',
            'name': '手术过程中异物遗留发生率',
            'numerator_description': '手术过程中异物遗留发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.11',
            'name': '手术患者麻醉并发症发生率',
            'numerator_description': '手术患者麻醉并发症发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.12',
            'name': '手术患者肺部感染与肺机能不全发生率',
            'numerator_description': '手术患者肺部感染与肺机能不全发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.13',
            'name': '手术意外穿刺伤或撕裂伤发生率',
            'numerator_description': '手术意外穿刺伤或撕裂伤发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.14',
            'name': '手术后急性肾衰竭发生率',
            'numerator_description': '手术后急性肾衰竭发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.15',
            'name': '各系统/器官术后并发症发生率',
            'numerator_description': '手术患者消化、循环、神经、眼和附器、耳和乳突、肌肉骨骼、泌尿生殖、口腔等系统/ 器官术后并发症发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.16',
            'name': '植入物的并发症（不包括脓毒症）发生率',
            'numerator_description': '植入物的并发症（不包括脓毒症）发生例数',
            'denominator_description': '同期手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.17',
            'name': '再植和截肢的并发症发生率',
            'numerator_description': '再植和截肢的并发症发生例数',
            'denominator_description': '同期再植和截肢患者出院人数',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.18',
            'name': '介入操作与手术患者其他并发症发生率',
            'numerator_description': '介入操作与手术患者其他并发症发生例数',
            'denominator_description': '同期介入操作与手术患者出院人次',
            'category_id': category_ids['C']
        },
        {
            'code': 'C11.19',
            'name': '剖宫产分娩产妇产程和分娩并发症发生率',
            'numerator_description': '剖宫产分娩产妇产程和分娩并发症发生例数',
            'denominator_description': '同期剖宫产分娩产妇出院人数',
            'category_id': category_ids['C']
        },
        # D类指标
        {
            'code': 'D01',
            'name': '门诊病历电子化比例',
            'numerator_description': '门诊患者使用电子化病历记录的人次数',
            'denominator_description': '同期门诊患者人次数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D02',
            'name': '门诊结构化病历使用比例',
            'numerator_description': '门诊患者使用结构化电子病历记录的人次数',
            'denominator_description': '同期门诊患者人次数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D03',
            'name': '病案首页主要诊断编码正确率',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['D']
        },
        {
            'code': 'D03.1',
            'name': '病案首页主要诊断填写正确率',
            'numerator_description': '病案首页中主要诊断填写正确的出院患者病历数',
            'denominator_description': '同期出院患者病历总数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D03.2',
            'name': '病案首页主要诊断编码正确率',
            'numerator_description': '病案首页中主要诊断编码正确的出院患者病历数',
            'denominator_description': '同期出院患者病历总数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D04',
            'name': '病历记录及时性',
            'numerator_description': '',
            'denominator_description': '',
            'category_id': category_ids['D']
        },
        {
            'code': 'D04.1',
            'name': '入院记录24小时内完成率',
            'numerator_description': '入院记录在患者入院24小时内完成的住院患者病历数',
            'denominator_description': '同期住院患者病历总数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D04.2',
            'name': '手术记录24小时内完成率',
            'numerator_description': '手术记录在术后24小时内完成的住院患者病历数',
            'denominator_description': '同期住院手术患者病历总数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D04.3',
            'name': '出院记录24小时内完成率',
            'numerator_description': '出院记录在患者出院后24小时内完成的病历数',
            'denominator_description': '同期出院患者病历总数',
            'category_id': category_ids['D']
        },
        {
            'code': 'D04.4',
            'name': '病案首页24小时内完成率',
            'numerator_description': '病案首页在患者出院后24小时内完成的病历数',
            'denominator_description': '同期出院患者病历总数',
            'category_id': category_ids['D']
        }
    ]
    
    # 更新或创建指标
    for indicator_data in indicators:
        indicator = Indicator.query.filter_by(code=indicator_data['code']).first()
        if indicator:
            # 更新现有指标
            indicator.name = indicator_data['name']
            indicator.numerator_description = indicator_data['numerator_description']
            indicator.denominator_description = indicator_data['denominator_description']
            indicator.category_id = indicator_data['category_id']
        else:
            # 创建新指标
            indicator = Indicator(**indicator_data)
            db.session.add(indicator)
    
    # 提交更改
    db.session.commit()
    print("所有指标信息已更新完成！")

if __name__ == '__main__':
    update_all_indicators() 