<template>
  <el-container>
    <el-main>
      <component :is="GroupCard">

      </component>

    </el-main>
  </el-container>

</template>

<script lang="ts" setup name="group">
import GroupCard from "./GroupCard/index.vue";

interface DataInterface {
  id: number;
  name: string;
  project: number;
  type: number;
  typeDESC: string;
  description: string;
  creator_name: string;
  count: number;
  nodeId: string;
  nodeName: string;
}

interface CusResponseInter {
  code: number;
  msg: string;
  page: number;
  limit: number;
  total: number;
  is_next: boolean;
  is_previous: boolean;
  data: DataInterface[];
}

const webOrInterTypes = [
  {
    'value': 0,
    'label': 'Web'
  },
  {
    'value': 1,
    'label': 'Inter'
  }
];

let NodeModalVisible = false;
const formRules = {
  name: [{
    required: true,
    message: "名称是必填项!",
    trigger: "blur"
  }],
  project: [{
    required: true,
    message: "项目是必填项!",
    trigger: "blur"
  }],
  type: [{
    required: true,
    message: "类型是必选的",
    trigger: "blur"
  }],
  description: [{
    required: false,
    message: "描述是非必填项!",
    trigger: "blur"
  }]
};
const caseItemModel = {};
let caseItemModalVisible = false;

</script>
<style lang="scss" scoped>
.el-header {
  color: #333;
  line-height: 60px;
}

.el-main {
  height: calc(100vh - 80px);
  overflow: hidden;
  background-color: #f0f2f5;

  .module-card {
    height: calc(100vh - 355px);
    margin-top: 32px;

    & ::v-deep .el-card__body {
      height: calc(100vh - 428px);
      overflow-y: auto;
    }

    .module-header {
      display: flex;
      padding: -6px 20px;
      align-items: center;
      justify-content: space-between;
    }
  }
}

.avatar-uploader ::v-deep .el-upload {
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.avatar-uploader ::v-deep .el-upload:hover {
  border-color: #409EFF;
}

.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 48px;
  line-height: 48px;
  text-align: center;
}

.avatar {
  width: 178px;
  height: 178px;
  display: block;
}
</style>
