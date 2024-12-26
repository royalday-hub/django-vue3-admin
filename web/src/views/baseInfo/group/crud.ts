import { CrudOptions, AddReq, DelReq, EditReq, dict, CrudExpose, compute } from '@fast-crud/fast-crud';
import _ from 'lodash-es';
import * as api from './api';
import { dictionary } from '/@/utils/dictionary';
import {inject} from "vue";
import {successMessage} from "/@/utils/message";
interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

//此处为crudOptions配置
export const createCrudOptions = function ({ crudExpose, rolePermission }: { crudExpose: CrudExpose; rolePermission: any }): CreateCrudOptionsTypes {
	const pageRequest = async (query: any) => {
		return await api.GetProjectList(query);
	};
	const editRequest = async ({ form, row }: EditReq) => {
		form.id = row.id;
		return await api.UpdateObj(form);
	};
	const delRequest = async ({ row }: DelReq) => {
		return await api.DelObj(row.id);
	};
	const addRequest = async ({ form }: AddReq) => {
		return await api.AddObj(form);
	};

	//权限判定
	const hasPermissions = inject("$hasPermissions")

	// @ts-ignore
	// @ts-ignore
	return {
		crudOptions: {
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			rowHandle: {
				//固定右侧
				fixed: 'right',
				width: 200,
				buttons: {
					view: {
						show: false,
					},
					edit: {
						iconRight: 'Edit',
						type: 'text',
						show:hasPermissions('role:Update')
					},
					remove: {
						iconRight: 'Delete',
						type: 'text',
						show:hasPermissions('role:Delete')
					},
					custom: {
						text: '权限配置',
						type: 'text',
						show:hasPermissions('role:Update'),
						tooltip: {
							placement: 'top',
							content: '权限配置',
						},
						click: (context: any): void => {
							const { row } = context;
							// eslint-disable-next-line no-mixed-spaces-and-tabs
							rolePermission.value.drawer = true;
							rolePermission.value.editedRoleInfo = row;
							rolePermission.value.initGet();
						},
					},
				},
			},
			form: {
				col: { span: 24 },
				labelWidth: '100px',
				wrapper: {
					is: 'el-dialog',
					width: '600px',
				},
			},
			columns: {

			},
		},
	};
};
