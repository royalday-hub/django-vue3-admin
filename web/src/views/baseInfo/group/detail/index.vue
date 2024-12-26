<template>
    <el-container>
        <el-main>
            <el-drawer title="编辑参数" :visible.sync="drawer" size="50%">
                <div style="padding-left: 20px;">
                    <el-button icon="el-icon-plus" size="mini" @click="add_params()">添加</el-button>
                    <el-upload ref="upload"
                               class="avatar-uploader"
                               accept=".csv"
                               action="../mypro/api/case/uploadcsv"
                               :on-success="uploadRes"
                               :on-error="uploadError"
                               :auto-upload="true"
                               :show-file-list="false"
                               :limit="1"
                               :data=" csvData"
                               style="float: right;">
                        <el-button icon="el-icon-upload2" size="mini" style="float:right;margin-right: 30px;">导入csv
                        </el-button>
                    </el-upload>
                    <el-button icon="el-icon-download" size="mini" @click="export_csv()"
                               style="float:right;margin-right: 10px;">
                        导出csv
                    </el-button>
                    <vxe-table ref=" testData" style="padding-right: 20px;"
                               :data=" testData"
                               :edit-config="{trigger: 'dblclick', mode: 'row',showStatus: true,autoClear:false}"
                               @edit-closed="editCloseEvent" @edit-actived="editActiveEvent"
                               height="auto" border="none"
                               highlight-hover-row highlight-current-row keep-source>
                        <vxe-column field="key" title="参数" :edit-render="{name: 'input', immediate:true}"
                                    min-width="50%">
                        </vxe-column>
                        <vxe-column field="count" title="数量" width="25%" :edit-render="{ enabled: false }"></vxe-column>

                        <vxe-column title="操作" width="25%" :edit-render="{ enabled: false }">
                            <template v-slot="{ row }">
                                <i class="el-icon-edit" v-show="!row.isedit" style="color: royalblue;"
                                   @click="edit_params(row)"></i>&nbsp;
                                <i class="el-icon-delete" v-show="!row.isedit" style="color: royalblue;"
                                   @click="del_params(row)"></i>
                                <i class="el-icon-check" v-show="row.isedit" title="保存" style="color: royalblue;"
                                   @click.stop="saveParam(row)">
                                </i>&nbsp;
                                <i class="el-icon-close" v-show="row.isedit" title="取消" style="color: royalblue;"
                                   @click.stop="cancelParam(row)">
                                </i>
                            </template>
                        </vxe-column>
                    </vxe-table>
                    <el-drawer :title="'编辑参数【'+ rowData.key+'】'" :append-to-body="true" :before-close="handleClose2"
                               :visible.sync="innerDrawer" size="40%">
                        <div style="padding-left: 20px;">
                            <el-button icon="el-icon-plus" size="mini" @click="add_value()">添加</el-button>
                            <el-button icon="el-icon-check" size="mini" @click="save_value()">保存</el-button>
                            <vxe-table ref=" paramData" style="padding-right: 20px;" :data=" paramData"
                                       :edit-config="{trigger: 'dblclick', mode: 'row',showStatus: true,autoClear:false}"
                                       height="auto" border="none" highlight-hover-row highlight-current-row
                                       :seq-config="{startIndex: 0}" @edit-actived="editActiveValue" keep-source>
                                <vxe-column type="seq" min-width="20%"></vxe-column>
                                <vxe-column field="value" title="值" width="50%"
                                            :edit-render="{name: 'input', immediate:true}"></vxe-column>
                                <vxe-column title="操作" width="30%" :edit-render="{ enabled: false }">
                                    <template v-slot="{ row }">
                                        <i class="el-icon-delete" v-show="!row.isedit" style="color: royalblue;"
                                           @click="del_value(row)"></i>
                                    </template>
                                </vxe-column>
                            </vxe-table>
                        </div>
                    </el-drawer>
                </div>
            </el-drawer>


            <!--  顶部   -->
            <div @dblclick="changeModuleCanUpdate"
                 style="width: 100%; display: flex; flex-direction: row; justify-content: space-between; background-color: white">
                <!-- 模块栏 -->
                <div style="flex: 1;overflow-x: scroll;height: 100%" class="my-scrollbar">
                    <draggable v-model="moduleList" group="moduleList"
                               @start="drag=true" @end="draggableEnd"
                               :forceFallback="true"
                               item-key="id"
                               delay="200"
                               style="border-bottom: 2px solid #1890ff;white-space: nowrap;">
                        <el-input v-for="(module,index) in moduleList" v-model="module.moduleName"
                                  :key="index"
                                  :value="module.moduleName"
                                  placeholder="默认模块"
                                  class="draggableInput"
                                  :class="selectedModuleIndex===index ? 'selectedInput':'input'"
                                  readonly
                                  @blur="toUpdateModule($event, index)"
                                  @focus="selectedModule(index)">
                        </el-input>
                    </draggable>
                </div>

                <div
                        style="background: white;width: 400px;height: 42px; display: flex; flex-direction: row; justify-content: space-between">
                    <el-input style="width: 280px;padding-right: 2px;margin: 0px" placeholder="请输入用例名称.."
                              v-model="searchKey" @keyup.native="searchEvent($event)">
                        <el-button slot="append" icon="el-icon-search"></el-button>
                    </el-input>

                    <!--  添加模块        -->
                    <el-tooltip class="item" effect="dark" content="添加模块" placement="top-start"
                                style="padding: 5px 25px 5px 5px;margin: 5px">
                        <el-button icon="el-icon-plus" size="mini" @click="createModule()"
                                   :disabled="isDisableCreateModule">
                            添加
                        </el-button>
                    </el-tooltip>
                    <el-button icon="el-icon-delete" size="mini" type="danger"
                               style="padding: 5px 10px 5px 5px;margin: 5px"
                               @click="deleteCase()">
                        批量删除
                    </el-button>
                    <!--          todo 完善其他操作-->
                    <!--  其他操作        -->
                    <el-tooltip class="item" effect="dark" content="其他操作" placement="top-start">
                        <el-popover placement="bottom" title="模块操作" width="100" trigger="click"
                                    content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。">

                            <el-button icon="el-icon-delete" size="mini"
                                       style="width: calc(100%); margin: 8px 2px 8px 2px;"
                                       @click="deleteModule()">
                                删除模块
                            </el-button>

                            <el-button icon="el-icon-circle-check" size="mini"
                                       style="width: calc(100%); margin: 8px 2px 8px 2px;"
                                       @click="toSortModule()">
                                保存拖拽
                            </el-button>

                            <el-button icon="el-icon-circle-check" size="mini"
                                       style="width: calc(100%); margin: 8px 2px 8px 2px;"
                                       @click="get_datas()">
                                参数化
                            </el-button>

                            <i class="el-icon-more" slot="reference"
                               style="transform:rotate(90deg);position: relative;top: 22%;"></i>

                        </el-popover>
                    </el-tooltip>
                </div>
            </div>

            <el-card style="height: calc(100vh - 160px);">
                <!--        todo 树形表格数据更新后展开行不变处理 -->
                <vxe-table show-overflow ref="caseTableRef"
                           :row-config="{isHover: true, keyField: 'typeWithId'}"
                           :tree-config="{children: 'groupStep', trigger: 'cell', reserve: true, expandAll: true }"
                           :expand-config="{reserve: true, expandAll:true}"
                           :edit-config="{ trigger: 'dblclick', mode: 'row', showStatus: true, autoClear:false}"
                           @edit-closed="editCloseEvent"
                           @edit-actived="editActiveEvent"
                           :checkbox-config="{ labelField: 'indexId' }"
                           height="auto"
                           :data="caseList"
                           highlight-hover-row
                           highlight-current-row
                           :keep-source="true">
                    <vxe-table-column type="checkbox" title="编号" min-width="80px" tree-node></vxe-table-column>
                    <vxe-table-column field="name" title="标题" min-width="200px"
                                      :edit-render="{ name: 'input', autoSelect:true, immediate:true }">
                    </vxe-table-column>
                    <vxe-table-column min-width="120px" field="keywordName" title="关键字"
                                      :edit-render="{autofocus: '.custom-input',immediate: true}">
                        <template v-slot:edit="{ row }">
                            <el-select v-model="row.keyword" filterable clearable default-first-option
                                       v-show="row.type === 2">
                                <el-option v-for="item in keywordList" :key="item.id" :value="item.id"
                                           :label="item.name"/>
                            </el-select>
                        </template>
                    </vxe-table-column>
                    <vxe-table-column field="input_one" min-width="300px" title="步骤参数1"
                                      :edit-render="{ name: 'input_one',autoSelect:true,immediate:true }">
                    </vxe-table-column>
                    <vxe-table-column field="input_two" min-width="260px" title="步骤参数2"
                                      :edit-render="{ name: 'input_two',autoSelect:true,immediate:true }">
                    </vxe-table-column>
                    <vxe-table-column field="input_three" min-width="260px" title="步骤参数3"
                                      :edit-render="{ name: 'input_three',autoSelect:true,immediate:true }">
                    </vxe-table-column>
                    <vxe-table-column field="creator_name" title="作者/参数" min-width="100px"
                                      :edit-render="{ name: 'creator_name',autoSelect:true,immediate:true,props: {disabled: authorDisabled } }">
                    </vxe-table-column>


                    <vxe-table-column title="操作" min-width="200px" :edit-render="{ enabled: false }" allAlign="left"
                    >
                        <template v-slot:header>
                            <el-tooltip class="item" effect="dark" content="添加用例" placement="top-start">
                                <el-button icon="el-icon-plus" type="success" size="mini"
                                           @click="showAddCaseOrStepDialog(1)">添加用例
                                </el-button>
                            </el-tooltip>

                            <el-tooltip class="item" effect="dark" content="保存拖拽" placement="top-start">
                                <el-button icon="el-icon-rank" type="primary" size="mini" @click="toSortCaseAndStep()">
                                    保存拖拽
                                </el-button>
                            </el-tooltip>
                        </template>
                        <template v-slot="{ row }">

                            <el-tooltip class="item" effect="dark" content="编辑" placement="top">
                                <el-button size="small" title="编辑" v-show="!row.isedit" type="primary" circle plain
                                           icon="el-icon-edit" style="font-weight: bold;"
                                           @click.stop="showEditCaseOrStep(row)">
                                </el-button>
                            </el-tooltip>
                            <el-tooltip class="item" effect="dark" content="保存" placement="top">
                                <el-button v-show="row.isedit" title="保存" size="small" type="success" circle
                                           icon="el-icon-check" style="font-weight: bold;"
                                           @click.stop="addAndUpdateCaseOrStep(row)">
                                </el-button>
                            </el-tooltip>

                            <el-tooltip class="item" effect="dark" content="取消" placement="top">
                                <el-button size="small" type="danger" circle v-show="row.isedit" icon="el-icon-close"
                                           style="font-weight: bold;"
                                           @click.stop="cancelAddAndUpdateCaseOrStep(row)"></el-button>
                            </el-tooltip>

                            <el-tooltip class="item" effect="dark" content="新增步骤" placement="top">
                                <el-button size="small" type="success" circle v-show="!row.isedit && row.type === 1"
                                           icon="el-icon-plus"
                                           style="font-weight: bold;" @click="showAddCaseOrStepDialog(2, row)">
                                </el-button>
                            </el-tooltip>

                            <el-tooltip class="item" effect="dark" content="删除" placement="top">
                                <el-button size="small" type="danger" circle
                                           icon="el-icon-delete" v-show="!row.isedit"
                                           style="font-weight: bold" @click="deleteCase(row)">
                                </el-button>
                            </el-tooltip>
                        </template>
                    </vxe-table-column>
                </vxe-table>
            </el-card>
        </el-main>

        <el-dialog :title="(caseOrStepItemModel.add ? '新增' : '编辑') + (caseOrStepItemModel.type === 1 ? '用例' : '步骤3123')"
                   :visible.sync="caseItemModalVisible">
            <el-form ref="createUpdateCaseRef" :model="caseOrStepItemModel" label-position="left"
                     :rules="caseOrStepItemModel.type === 1 ? caseRules: stepRules"
                     label-width="150px"
                     style="width: 400px; margin-left:50px;">
                <el-form-item :label="caseOrStepItemModel.type === 1? '用例名称': '步骤名称'" prop="name">
                    <el-input v-model="caseOrStepItemModel.name"></el-input>
                </el-form-item>
                <el-form-item v-if="caseOrStepItemModel.type === 2" label="关键字" prop="keyword">
                    <el-select v-model="caseOrStepItemModel.keyword" filterable clearable default-first-option
                               style="display: block; width: 100%;"
                    >
                        <el-option v-for="item in keywordList" :key="item.id" :value="item.id" :label="item.name"/>
                    </el-select>
                    <!--          <el-input v-model="caseOrStepItemModel.keyword"></el-input>-->
                </el-form-item>
                <el-form-item v-if="caseOrStepItemModel.type === 2" label=" 参数1" prop="input_one">
                    <el-input v-model="caseOrStepItemModel.input_one"></el-input>
                </el-form-item>
                <el-form-item v-if="caseOrStepItemModel.type === 2" label=" 参数2" prop="input_two">
                    <el-input v-model="caseOrStepItemModel.input_two"></el-input>
                </el-form-item>
                <el-form-item v-if="caseOrStepItemModel.type === 2" label=" 参数3" prop="input_three">
                    <el-input v-model="caseOrStepItemModel.input_three"></el-input>
                </el-form-item>
            </el-form>
            <div slot="footer" class="dialog-footer">
                <el-button @click="cancelAddAndUpdateCaseOrStep(footer)">
                    取消
                </el-button>
                <el-button type="primary" @click="addAndUpdateCaseOrStep()">
                    确定
                </el-button>
            </div>
        </el-dialog>
    </el-container>
</template>

<script lang="ts" setup name="groupDetail">
    import {ref, onMounted, onBeforeUnmount, Ref} from 'vue';
    import {useRoute} from 'vue-router';
    import XEUtils from "xe-utils";
    import Sortable from "sortablejs";
    import draggable from 'vuedraggable'
    import {infoMessage, errorMessage} from '/@/utils/message';
    import {
        GetModuleList,
        GetModuleCaseList,
        AddModuleObj,
        AddCaseObj,
        AddStepObj,
        UpdateModule,
        UpdateCase,
        UpdateStep,
        sortModule,
        sortCaseStep,
        DelModule, DelCaseOrStep, MultipleDelCaseOrStep
    } from "./api";

    import {GetList} from '../../baseInfo/keyword/api'

    const route = useRoute();
    let caseTableRef = ref();
    // 用例组id
    let groupId: any = 0;
    // 当前选择的模块;
    let selectedModuleIndex: 0;
    // 是否可以编辑模块;
    let isUpdateModule = false;
    let drawer = false;
    let innerDrawer = false;
    let testData = [];
    let paramData = [];
    let isEditValue = false;
    let rowData = {};
    let csvData = {'groupId': groupId};

    let tabIndex = 0;
    let searchKey = "";
    let activeIndex = "";
    let keywordList = [];
    // 模块列表
    let moduleList: any = [{
        id: 1,
        moduleName: '暂无模块'
    }];
    let maxModuleSort = 0;
    let isDisableCreateModule = false;
    // 用例列表
    let caseList = [];
    let originCaseDatas: [];

    let listLoading =;
    // 新增编辑用例弹窗显示状态
    let caseItemModalVisible = false;
    let caseOrStepItemModel = {};
    let edit_row = [];
    let isSort = false;
    let authorDisabled = true;
    let caseTableSortAble: any = null;


    let caseRules = {
        name: [
            {
                required: true,
                message: "用例名是必填项!",
                trigger: "blur"
            },
        ],
    };
    let stepRules = {
        name: [
            {
                required: true,
                message: "步骤名是必填项!",
                trigger: "blur"
            },
        ],
        keyword: [
            {
                required: true,
                message: "关键字是必填项!",
                trigger: "blur"
            },
        ]
    };
    type resType = { data: { data: any[] } };

    // 设置用例行可拖动
    const setCaseTableSort = (tableComponent: Ref<any>, tableTreeData: any[]) => {
        // 表格拖拽排序的
        const el = tableComponent.value.$el.querySelectorAll(
            ".vxe-table--body-wrapper > table > tbody"
        )[0];
        caseTableSortAble = Sortable.create(el, {
            ghostClass: "sortable-ghost", // Class name for the drop placeholder,
            setData: function (dataTransfer) {
                dataTransfer.setData("Text", "");
            },
            onEnd: ({
                        item,
                        oldIndex
                    }) => {
                const options = {
                    children: "groupStep"
                };
                const targetTrElem = item;
                const wrapperElem: any = targetTrElem.parentNode;

                const prevTrElem = targetTrElem.previousElementSibling;
                const selfRow = tableComponent.value.getRowNode(targetTrElem).item;
                const selfNode = XEUtils.findTree(
                    tableTreeData,
                    (row) => row === selfRow,
                    options
                );
                if (prevTrElem) {
                    // 移动到节点
                    const prevRow = tableComponent.value.getRowNode(<HTMLElement>prevTrElem).item;
                    const prevNode = XEUtils.findTree(
                        tableTreeData,
                        (row) => row === prevRow,
                        options
                    );

                    console.log("selfRow", selfRow)
                    console.log("selfNode", selfNode)
                    console.log("prevRow", prevRow)
                    console.log("prevNode", prevNode)
                    // 不允许步骤移动到用例中
                    if (prevRow.parent !== selfRow.parent) {
                        tableComponent.value.syncData();
                        return infoMessage("不允许跨用例拖动！")
                    }

                    if (
                        XEUtils.findTree(
                            selfRow[options.children],
                            (row) => prevRow === row,
                            options
                        )
                    ) {
                        // 错误的移动
                        if (oldIndex) {
                            const oldTrElem = wrapperElem.children[oldIndex];
                            wrapperElem.insertBefore(targetTrElem, oldTrElem);
                            return errorMessage("不允许自己给自己拖动！")
                        }
                    }


                    const currRow = selfNode.items.splice(selfNode.index, 1)[0];
                    if (tableComponent.value.isTreeExpandByRow(prevRow)) {
                        // 移动到当前的子节点
                        prevRow[options.children].splice(0, 0, currRow);
                    } else {
                        // 移动到相邻节点
                        prevNode.items.splice(
                            prevNode.index + (selfNode.index < prevNode.index ? 0 : 1),
                            0,
                            currRow
                        );
                    }
                } else {
                    // 移动到第一行
                    const currRow = selfNode.items.splice(selfNode.index, 1)[0];
                    tableTreeData.unshift(currRow);
                }
                // 如果变动了树层级，需要刷新数据
                tableComponent.value.syncData();
                console.log('拖动了');
                isSort = true;
            },
        });

    }
    // 设置用例行可拖动
    const initCaseTableSortAble = (data: any[]) => {
        if (caseTableSortAble) {
            caseTableSortAble.destroy();
        }
        // this.$nextTick(() => {
        setCaseTableSort(caseTableRef, data);
        // });
    };
    // 获取用例组用例列表
    const getCases = (moduleIndex: number) => {
        GetModuleCaseList({"module": moduleList[moduleIndex].id}).then((res: resType) => {
            caseList = res.data.data;
            initCaseTableSortAble(res.data.data);

        }).catch((e: any) => {
            console.log(e);
        });
    }
    // 获取模块列表
    const getModules = () => {
        isDisableCreateModule = true;
        GetModuleList({"group": groupId}).then((res: { data: { data: any; }; }) => {
            moduleList = res.data.data;
            maxModuleSort = moduleList[moduleList.length - 1].sort
            getCases(selectedModuleIndex);
        }).catch((e) => {
            console.log(e);
        });
        isDisableCreateModule = false
        // location.reload()
    }
    onMounted(() => {
        groupId = route.params.groupId;
        getModules();
        getKeywordList();
    })

    onBeforeUnmount(() => {
        if (caseTableSortAble) {
            caseTableSortAble.destroy();
        }
    });


    // 取消新增或编辑用例和步骤
    cancelAddAndUpdateCaseOrStep(row = null)
    {
        this.caseItemModalVisible = false
        // this.$refs['caseTableRef'].revertData()
        // 解决取消编辑后，列表展开行会被重置，展示重新获取数据解决
        this.getCases(this.selectedModuleIndex)
    }

    // 重新选择模块,拖拽事件
    reSelectModule()
    {
        if (this.selectedModuleIndex === 0) {
            this.selectedModuleIndex = 0
        } else {
            this.selectedModuleIndex = this.selectedModuleIndex - 1
        }
    }

    draggableEnd(e)
    {
        // console.log(e)
        this.selectedModuleIndex = e.newIndex
        if (e.newIndex !== e.oldIndex) {
            this.toSortModule()
        }

    }
    // 获取关键字列表
    getKeywordList()
    {
        GetList({"limit": 999})
            .then((res) => {
                console.log(res);
                this.keywordList = res.data.data;
            })
            .catch((e) => {
                console.log(e)
                this.loading = false
            })
    }

    export_csv()
    {
        window.open('/mypro/api/case/exportcsv?groupId=' + this.groupId);
    }

    uploadRes(res)
    {
        if (res.code === 1000) {
            // 上传成功后，更新参数
            this.$nextTick(() => {
                this.$refs.upload.clearFiles();
                this.$message({
                    type: "success",
                    message: res.msg,
                });
                this.get_datas();
            })
        } else {
            this.$message({
                type: "error",
                message: res.msg,
                duration: 3 * 1000
            });
            this.$refs.upload.clearFiles();
        }
    }

    uploadError(err)
    {
        this.$refs.upload.clearFiles();
        this.$message({
            type: "error",
            message: "服务器忙：" + err.status,
        });
    }

    get_datas()
    {
        this.$store.dispatch('case/getdatas', this.groupId)
            .then((res) => {
                this.drawer = true;
                for (let i = 0; i < res.length; i++) {
                    res[i].count = res[i].value.length;
                }
                this.testData = [...res];
            })
            .catch((e) => {
                console.log(e);
            });
    }

    editActiveValue()
    {
        this.isEditValue = true;
    }

    handleClose2(done)
    {
        if (!this.isEditValue) {
            done();
            return;
        }
        this.$confirm('还有未保存的工作哦确定关闭吗？')
            .then(_ => {
                done();
            })
            .catch(_ => {
            });
    }

    add_params()
    {
        this.testData.push({
            'key': 'param_name',
            'count': -1
        });
    }

    add_value()
    {
        this.paramData.push({
            'idx': this.paramData.length + 1,
            'value': '请输入参数值',
        });
    }

    del_value(row)
    {
        console.log(row);
        this.paramData.splice(this.paramData.indexOf(row), 1);
    }

    save_value()
    {
        let values = [];
        for (let i = 0; i < this.paramData.length; i++) {
            values.push(this.paramData[i].value);
        }
        console.log(values);
        this.$store.dispatch('case/savevalue', {
            'id': this.rowData.id,
            'value': values
        })
            .then((res) => {
                this.$message({
                    type: "success",
                    message: "保存成功...",
                    duration: 2 * 1000
                });
                this.isEditValue = false;
                this.innerDrawer = false;
                this.get_datas();
            });
    }

    edit_params(data)
    {
        console.log(data);
        this.innerDrawer = true;
        this.paramData = []
        for (let i = 0; i < data.value.length; i++) {
            this.paramData.push({
                'idx': i + 1,
                'value': data.value[i]
            });
        }
        this.rowData = data;
    }

    del_params(data)
    {
        console.log(data);
        this.$store.dispatch('case/deletekey', data.id)
            .then((res) => {
                this.$message({
                    type: "success",
                    message: "删除成功...",
                    duration: 2 * 1000
                });
                this.get_datas();
            });
    }

    cancelParam(row)
    {
        this.$refs.testData.clearActived().then(() => {
            // 还原行数据，暂时只能还原整个用例的，如果要还原步骤，请取消一下用例的编辑
            this.$refs.testData.revertData(row);
        })
    }

    saveParam(row)
    {
        console.log(row)
        let data = {
            id: row.id,
            groupId: this.groupId,
            key: row.key,
        }
        this.$store.dispatch('case/updatekey', data)
            .then((res) => {
                row.isedit = false;
                this.$refs.testData.clearActived();
            });
    }

    // 操作模块是否可以编辑
    changeModuleCanUpdate(event)
    {
        // 事件响应的元素
        let ele = event.target;
        ele.readOnly = false;
        ele.select();
        this.isUpdateModule = true;
    }

    // 编辑模块
    toUpdateModule(event, index)
    {
        if (!this.isUpdateModule) {
            return;
        }
        console.log(event, index)
        console.log(index)
        let moduleObj = this.moduleList[index]
        moduleObj["name"] = moduleObj["moduleName"]
        UpdateModule(moduleObj)
            .then((res) => {
                // 事件响应的元素
                let ele = event.target;
                ele.readOnly = true;
            })
            .catch((e) => {
                console.log(e);
            });
        this.isUpdateModule = false
    }

    // 选中模块
    selectedModule(index)
    {
        if (this.selectedModuleIndex !== index) {
            this.selectedModuleIndex = index;
            this.getCases(index);
        }
    }

    // 删除模块
    deleteModule()
    {
        const that = this
        this.$confirm(`你确定要删除当前选中的模块吗?`, "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
        })
            .then(() => {
                that.$message({
                    type: "info",
                    message: "正在删除模块：" + that.moduleList[that.selectedModuleIndex].moduleName,
                    duration: 2 * 1000
                });

                DelModule(that.moduleList[that.selectedModuleIndex].id)
                    .then((res) => {
                        that.getModules();
                        that.reSelectModule()
                        that.$message({
                            type: "success",
                            message: res.msg,
                            duration: 2 * 1000
                        });
                    });
            })
            .catch(() => {
                that.$message({
                    type: "info",
                    message: "已取消删除",
                    duration: 2 * 1000
                });
            });
    }

    // 保存模块排序
    toSortModule()
    {
        let tempModuleIdList = [];
        // 获取到模块列表的ids
        for (let i = 0; i < this.moduleList.length; i++) {
            tempModuleIdList.push(this.moduleList[i].id);
        }
        sortModule(tempModuleIdList)
            .then((res) => {
                this.getModules();
                this.$message({
                    type: "success",
                    message: res.msg,
                    duration: 2 * 1000
                });
            });
    }

    toSortCaseAndStep()
    {
        let tempCaseStepDic = {};
        let tempCaseList = [];
        // 获取到模块列表的ids
        for (let i = 0; i < this.caseList.length; i++) {
            let case_obj = this.caseList[i]
            let temp = []
            tempCaseList.push(case_obj.id)
            for (let j = 0; j < case_obj["groupStep"].length; j++) {
                temp.push(case_obj["groupStep"][j].id);
            }
            tempCaseStepDic[case_obj.id] = temp
        }
        sortCaseStep(tempCaseStepDic, tempCaseList)
            .then((res) => {
                this.getCases(this.selectedModuleIndex);
                this.$message({
                    type: "success",
                    message: res.msg,
                    duration: 2 * 1000
                });
            });
    }


    // 新增模块
    createModule()
    {
        this.isDisableCreateModule = true
        const that = this
        let tempModule = {
            sort: this.moduleList.length,
            name: '新增模块',
            group: this.groupId
        }
        AddModuleObj(tempModule).then((res) => {
            that.getModules()
            tempModule = {}
            that.selectedModuleIndex = that.moduleList.length
            that.maxModuleSort = that.maxModuleSort + 1
        }).catch((e) => {
            console.log(e);
        });
        this.isDisableCreateModule = false
    }
    // 获取用例组用例列表
    getCases(moduleIndex)
    {
        GetModuleCaseList({"module": this.moduleList[moduleIndex].id}).then((res) => {
            this.caseList = res.data.data
            this.initCaseTableSortAble(res.data.data);

        }).catch((e) => {
            console.log(e);
        });
    }


    // 设置用例行可拖动
    setCaseTableSort(tableComponent, tableTreeData)
    {
        // 表格拖拽排序的
        const el = tableComponent.$el.querySelectorAll(
            ".vxe-table--body-wrapper > table > tbody"
        )[0];
        this.caseTableSortAble = Sortable.create(el, {
            ghostClass: "sortable-ghost", // Class name for the drop placeholder,
            setData: function (dataTransfer) {
                dataTransfer.setData("Text", "");
            },
            onEnd: ({
                        item,
                        oldIndex
                    }) => {
                const options = {
                    children: "groupStep"
                };
                const targetTrElem = item;
                const wrapperElem = targetTrElem.parentNode;

                const prevTrElem = targetTrElem.previousElementSibling;
                const selfRow = tableComponent.getRowNode(targetTrElem).item;
                const selfNode = XEUtils.findTree(
                    tableTreeData,
                    (row) => row === selfRow,
                    options
                );
                if (prevTrElem) {
                    // 移动到节点
                    const prevRow = tableComponent.getRowNode(prevTrElem).item;
                    const prevNode = XEUtils.findTree(
                        tableTreeData,
                        (row) => row === prevRow,
                        options
                    );

                    console.log("selfRow", selfRow)
                    console.log("selfNode", selfNode)
                    console.log("prevRow", prevRow)
                    console.log("prevNode", prevNode)
                    // 不允许步骤移动到用例中
                    if (prevRow.parent !== selfRow.parent) {
                        tableComponent.syncData();
                        return this.$message({
                            message: "不允许跨用例拖动！",
                            type: "error",
                            duration: 2 * 1000
                        });
                    }

                    if (
                        XEUtils.findTree(
                            selfRow[options.children],
                            (row) => prevRow === row,
                            options
                        )
                    ) {
                        // 错误的移动
                        const oldTrElem = wrapperElem.children[oldIndex];
                        wrapperElem.insertBefore(targetTrElem, oldTrElem);
                        return this.$XModal.message({
                            message: "不允许自己给自己拖动！",
                            status: "error",
                        });
                    }


                    const currRow = selfNode.items.splice(selfNode.index, 1)[0];
                    if (tableComponent.isTreeExpandByRow(prevRow)) {
                        // 移动到当前的子节点
                        prevRow[options.children].splice(0, 0, currRow);
                    } else {
                        // 移动到相邻节点
                        prevNode.items.splice(
                            prevNode.index + (selfNode.index < prevNode.index ? 0 : 1),
                            0,
                            currRow
                        );
                    }
                } else {
                    // 移动到第一行
                    const currRow = selfNode.items.splice(selfNode.index, 1)[0];
                    tableTreeData.unshift(currRow);
                }
                // 如果变动了树层级，需要刷新数据
                tableComponent.syncData();
                console.log('拖动了');
                this.isSort = true;
            },
        });

    }

    deleteCase(row = null)
    {
        // 获取到选中的用例的id列表
        console.log('debug');
        let that = this

        that.$confirm(`你确定要删除当前选中的所有用例吗?`, "提示", {
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            type: "warning",
        })
            .then(() => {
                that.$message({
                    type: "info",
                    message: "正在删除用例...",
                    duration: 2 * 1000
                });
                if (row) {
                    DelCaseOrStep(row.id, row.type).then((res) => {
                        that.getCases(this.selectedModuleIndex);
                        that.$message({
                            type: "success",
                            message: res.msg,
                            duration: 2 * 1000
                        });
                    });
                } else {
                    let tempCasList = [];
                    let tempStepList = [];
                    for (let i = 0; i < that.$refs['caseTableRef'].selection.length; i++) {
                        if (that.$refs['caseTableRef'].selection[i].type === 1) {
                            tempCasList.push(that.$refs['caseTableRef'].selection[i].id)
                        } else {
                            tempStepList.push(that.$refs['caseTableRef'].selection[i].id)
                        }
                    }
                    MultipleDelCaseOrStep(true, tempCasList, tempStepList)
                        .then((res) => {
                            that.getCases(this.selectedModuleIndex);
                            that.$message({
                                type: "success",
                                message: res.msg,
                                duration: 2 * 1000
                            });
                        });
                }
            })
            .catch(() => {
                that.$message({
                    type: "info",
                    message: "已取消删除",
                    duration: 2 * 1000
                });
            });
    }
    searchEvent(e)
    {
        let keyCode = e.keyCode || e.which || e.charCode;
        if (keyCode === 13) {
            //按下回车键执行内容
            console.log('查找')
        }
        // const filterName = XEUtils.toValueString(this.searchKey).trim().toLowerCase()
        // if (filterName) {
        //   const filterRE = new RegExp(filterName, 'gi')
        //   const options = {
        //     children: 'children'
        //   }
        //   const searchProps = ['stepName', 'keyword', 'input_one', 'input_two']
        //   const rest = XEUtils.searchTree(this.originCaseDatas, item => searchProps.some(key => XEUtils
        //     .toValueString(item[key]).toLowerCase().indexOf(filterName) > -1), options)
        //   XEUtils.eachTree(rest, item => {
        //     searchProps.forEach(key => {
        //       item[key] = XEUtils.toValueString(item[key])
        //     })
        //   }, options)
        //   // 列表显示为搜索出来的内容
        //   this.caseList = rest
        //   // 搜索之后默认展开所有子节点
        //   this.$nextTick(() => {
        //     this.$refs['caseTableRef'].setAllTreeExpand(true)
        //   })
        // } else {
        //   // 如果搜索没有关键词，就显示元素数据列表
        //   this.caseList = this.originCaseDatas;
        // }
    }

    editCloseEvent(data)
    {
        // console.log(data);
        data.row.isedit = false;
    }

    editActiveEvent({row})
    {
        row.isedit = true;
    }

    cancelRow(row)
    {
        this.$refs['caseTableRef'].clearActived().then(() => {
            // 还原行数据，暂时只能还原整个用例的，如果要还原步骤，请取消一下用例的编辑
            if (row.caseName) {
                this.$refs['caseTableRef'].revertData(row);
            }
        })
    }

    saveCase(row)
    {
        console.log("调用接口保存编辑: ", row);
        if (row.caseName) {
            let data = {
                id: row.id,
                caseName: row.stepName,
                keywordList: row.keyword,
            }
            this.$store.dispatch('case/updatecase', data)
                .then((res) => {
                    row.isedit = false;
                    this.$refs['caseTableRef'].clearActived();
                });
        } else {
            let data = {
                id: row.id,
                stepName: row.stepName,
                keywordList: row.keyword,
                input_one: row.input_one,
                input_two: row.author,
            }
            this.$store.dispatch('case/updatecase', data)
                .then((res) => {
                    row.isedit = false;
                    this.$refs['caseTableRef'].clearActived();
                });
        }
    }

    saveData()
    {
        const loading = this.$loading({
            lock: true,
            text: "保存中...",
            spinner: "el-icon-loading",
            background: "rgba(0, 0, 0, 0.7)",
        });
        setTimeout(() => {
            loading.close();
        }, 2000);
        console.log("保存的数据: ", this.moduleData[this.activeIndex]);
    }
    showAddCaseOrStepDialog(type, row = {})
    {
        // type: 1是用例，2是步骤
        if (type === 1) {
            this.caseOrStepItemModel = {
                'type': 1,
                'name': '新增用例',
                'add': true,
                'module': this.moduleList[this.selectedModuleIndex].id,
            };
        } else {
            // console.log("row", row)
            this.caseOrStepItemModel = {
                'type': 2,
                'name': '新增步骤',
                'add': true,
                'case': row.id,
            };
        }
        console.log("showAddCaseOrStepDialog", this.caseOrStepItemModel)
        this.caseItemModalVisible = true;
    }

    showEditCaseOrStep(data)
    {
        data.add = false;
        this.caseOrStepItemModel = data;
        this.caseItemModalVisible = true;
        this.$nextTick(() => {
            this.$refs['createUpdateCaseRef'].clearValidate();
        });
        console.log("showEditCaseOrStep", this.caseOrStepItemModel)
    }

    // 编辑和新增用例及步骤
    doSave(param)
    {
        if (param.add) {
            // 新增用例
            if (param.type === 1) {
                console.log("caseList", this.caseList)
                param["sort"] = this.caseList[this.caseList.length - 1].sort + 1
                AddCaseObj(param)
                    .then((res) => {
                        this.caseItemModalVisible = false;
                        this.getCases(this.selectedModuleIndex);
                        console.log("res", res)
                    });
                //  新增步骤
            } else {
                AddStepObj(this.caseOrStepItemModel)
                    .then((res) => {
                        this.caseItemModalVisible = false;
                        this.getCases(this.selectedModuleIndex);
                    });
            }
        } else {
            // 编辑用例
            if (param.type === 1) {
                UpdateCase(param)
                    .then((res) => {
                        this.caseItemModalVisible = false;
                        this.getCases(this.selectedModuleIndex);
                    });
                //  编辑步骤
            } else {
                UpdateStep(param)
                    .then((res) => {
                        this.caseItemModalVisible = false;
                        this.getCases(this.selectedModuleIndex);
                    });
            }
        }
    }
    addAndUpdateCaseOrStep(row = {})
    {
        console.log("this.caseOrStepItemModel", this.caseOrStepItemModel)
        if (JSON.stringify(row) !== "{}") {
            this.caseOrStepItemModel = row
            this.doSave(row)
            return
        }
        let param = this.caseOrStepItemModel
        this.$refs['createUpdateCaseRef'].validate((valid) => {
            if (valid) {
                console.log("调用接口保存变化: ", param);
                // 判断id是否存在来进行新增或编辑操作
                this.doSave(param)
            }
        })
    }
</script>

<style lang="scss">
    .el-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .my-dropdown {
        position: fixed;
        width: 150px;
        height: 300px;
        z-index: 20000;
        background: white;
        overflow: auto;
        border: 1px solid #75a3fc;
        border-top: 0;
    }

    .list-item {
        padding: 0 10px 10px 10px;
    }

    .class-case {
        background-color: red;
    }

    .el-main {
        background-color: #f0f2f5;
    }

    .input {
        border: none;
        text-align: center;
        top: 2px;
        position: relative;
        width: 100px;
    }

    .input > input {
        border: none;
        border-radius: 0;
        border-bottom: 2px solid #1890ff;
        text-align: center;
        cursor: pointer;

    }

    .input > input:hover {
        border: 2px solid yellow;
        background-color: #1890ff;
        border-radius: 0;
        color: yellow;
        margin: -1px;

    }

    .selectedInput {
        top: 2px;
        position: relative;
        width: 100px;

    }

    .selectedInput > input {
        border: none;
        border-radius: 0;
        border: 2px solid #1890ff;
        color: #1890ff;
        font-weight: bold;
        text-align: center;
        cursor: pointer;
        background-color: yellow;
    }

    .el-button--mini {
        padding: 7px 8px;
    }

    .keyword-lighten {
        background-color: yellow;
    }

    .my-scrollbar {
        &::-webkit-scrollbar {
            /*滚动条整体样式*/
            width: 4px; /*高宽分别对应横竖滚动条的尺寸*/
            height: 8px;
        }

        &::-webkit-scrollbar-thumb {
            /*滚动条里面小方块*/
            border-radius: 10px;
            box-shadow: inset 0 0 5px #00aaff;
            background: #409EFF;
        }

        &::-webkit-scrollbar-track {
            /*滚动条里面轨道*/
            box-shadow: inset 0 0 5px #1890ff;
            border-radius: 10px;
            background: #ededed;
        }

    }
</style>

<style scoped>
    /* 深度样式修改 */
    .el-card /deep/ .el-card__header {
        display: none;
    }

    .el-card /deep/ .el-card__body {
        height: 100%;
    }
</style>
