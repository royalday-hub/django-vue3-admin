import {downloadFile, request} from '/@/api/service';
import XEUtils from 'xe-utils'
export const urlPrefix = '/api/group/group/';

/**
 * 用例组列表查询
 */
export function GetProjectList(query) {
  return request({
    url: "/api/baseInfo/project/select/",
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
