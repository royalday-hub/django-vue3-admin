import {defineStore} from 'pinia';
import {BaseInfosStates, ProjectStates} from './interface';
import {Session} from '/@/utils/storage';
import {request} from '../utils/service';

/**
 * 用户信息
 * @methods setBaseInfs 设置项目信息
 */
export const useBaseInfo = defineStore('baseInfo', {
    state: (): BaseInfosStates => ({
        projects: []
    }),
    actions: {
        async updateProjects() {
            const that = this
            let projects: any = await this.GetProjectList();
            projects.data.forEach(function (item: ProjectStates, index: any) {
                that.projects.push({
                    id: item.id,
                    name: item.name
                })
            });
            Session.set('project', projects);
        },
        async setProjects() {
            const that = this
            // 存储用户信息到浏览器缓存
            if (Session.get('project')) {
                // 存储用户信息到浏览器缓存
                this.projects = Session.get('project');
            } else {
                let projects: any = await this.GetProjectList();
                projects.data.forEach(function (item: ProjectStates, index: any) {
                    that.projects.push({
                        id: item.id,
                        name: item.name
                    })
                });
                Session.set('project', this.projects);
            }
        },
        async GetProjectList() {
            return request({
                url: "/api/baseInfo/project/",
                method: 'get',
                params: {
                    page: 1,
                    limit: 999
                },
            });
        }
    },
});
