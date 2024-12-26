import { request } from '/@/utils/service';
import { PageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';
export const urlPrefix = '/api/group/group/';

/**
 * 用例组列表查询
 */
export function GetProjectList(query: PageQuery) {
  return request({
    url: "/api/baseInfo/project/select/",
    method: 'get',
    params: query

  })
}

/**
 * 新增
 */
export function AddObj(obj: AddReq) {
  return request({
    url: urlPrefix,
    method: 'post',
    data: obj
  })
}
/**
 * 修改
 */
export function UpdateObj(obj: EditReq) {
  return request({
    url: urlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}
/**
 * 删除
 */
export function DelObj(id: DelReq) {
  return request({
    url: urlPrefix + id + '/',
    method: 'delete',
    data: { id }
  })
}
