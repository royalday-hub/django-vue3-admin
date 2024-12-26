import {downloadFile, request} from '/@/api/service';
import XEUtils from 'xe-utils'
export const urlPrefix = '/api/baseInfo/group/';

/**
 * 列表查询
 */
export function GetList(query) {
  return request({
    url: urlPrefix,
    method: 'get',
    params: query
  })
}
/**
 * 新增
 */
export function AddObj(obj) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}
/**
 * 修改
 */
export function UpdateObj(obj) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}
/**
 * 删除
 */
export function DelObj(id) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}

export function BatchDel (keys) {
  return request({
    url: urlPrefix + 'multiple_delete/',
    method: 'delete',
    data: { keys }
  })
}

/**
 * 导出
 * @param params
 */
export function exportData (params) {
  const data = {
    // "case__module__project": params.project,
    // "case__name": params.name,
    // "case__module": params.module,
    "project": params['project'],
    "caseName": params['name'],
    "module": params['module'],
  };
  return downloadFile({
    url: urlPrefix + 'export/',
    params: data,
    method: 'post'
  })
}

/**
 * 获取用例统计
 * @param params
 */
export function GetChartList(query) {
  return request({
    url: urlChartPrefix,
    method: 'get',
    params: query
  }).then(res => {
    // 将列表数据转换为树形数据
    // console.log(res)
    res = res.data.data
    return res
  })
}
