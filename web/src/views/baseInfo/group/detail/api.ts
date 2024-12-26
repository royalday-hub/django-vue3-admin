import { request } from '/@/utils/service';
import { UserPageQuery, AddReq, DelReq, EditReq, InfoReq } from '@fast-crud/fast-crud';
import XEUtils from 'xe-utils'

export const urlPrefix = '/api/group/';
export const moduleUrlPrefix = '/api/group/groupModule/';
export const moduleCaseUrlPrefix = '/api/group/groupModuleCase/';
export const moduleCaseStepUrlPrefix = '/api/group/groupModuleCaseStep/';

/**
 * 获取用例组模块列表
 */
export function GetModuleList(query: UserPageQuery) {
  query["limit"] = 999
  return request({
    url: moduleUrlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 获取用例组模块-用例列表
 */
export function GetModuleCaseList(query: UserPageQuery) {
  query["limit"] = 999
  return request({
    url: moduleCaseUrlPrefix,
    method: 'get',
    params: query
  })
}

/**
 * 新增用例组模块
 */
export function AddModuleObj(obj: AddReq) {
  return request({
    url: moduleUrlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 新增用例组模块用例
 */
export function AddCaseObj(obj: AddReq) {
  return request({
    url: moduleCaseUrlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 新增用例组模块用例步骤
 */
export function AddStepObj(obj: AddReq) {
  return request({
    url: moduleCaseStepUrlPrefix,
    method: 'post',
    data: obj
  })
}

/**
 * 用例组模块保存排序
 */
export function sortModule(query: EditReq) {
  let data = {
    toSort: true,
    data: query
  }
  return request({
    url: moduleUrlPrefix,
    method: 'post',
    data: data
  })
}

/**
 * 用例组模块用例和步骤保存排序
 */
export function sortCaseStep(tempCaseStepDic: EditReq, tempCaseList: EditReq) {
  let data = {
    toSort: true,
    data: {
      caseStepDic: tempCaseStepDic,
      caseList: tempCaseList
    }
  }
  return request({
    url: moduleCaseUrlPrefix,
    method: 'post',
    data: data
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
 * 修改用例组模块
 */
export function UpdateModule(obj: EditReq) {
  return request({
    url: moduleUrlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 修改用例组模块用例
 */
export function UpdateCase(obj: EditReq) {
  return request({
    url: moduleCaseUrlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 修改用例组模块用例步骤
 */
export function UpdateStep(obj: EditReq) {
  return request({
    url: moduleCaseStepUrlPrefix + obj.id + '/',
    method: 'put',
    data: obj
  })
}

/**
 * 删除模块
 */
export function DelModule(id: DelReq) {
  return request({
    url: moduleUrlPrefix + id + '/',
    method: 'delete',
    data: {id}
  })
}
/**
 * 单个删除用例或步骤
 */
export function DelCaseOrStep(id: DelReq, type: DelReq) {
  let data = {
    type: type,
    id: id,
  }
  return request({
    url: moduleCaseUrlPrefix + id + '/',
    method: 'delete',
    data: data
  })

}
/**
 * 批量删除用例或步骤
 */
export function MultipleDelCaseOrStep(isMany = false, tempCasList = [], tempStepList = []) {
  let data = {
    many: isMany,
    casList: tempCasList,
    stepList: tempStepList
  }
  return request({
    url: moduleCaseUrlPrefix + "multiple_delete/",
    method: 'delete',
    data: data
  })

}
