<template>
      <div class="projectDropdownList">
        <el-dropdown  trigger="click" size="large" @command="handleDropdownCommand">
          <span>
            {{selectedProject?selectedProject.name:"管理项目"}}
            <el-icon class="el-icon--right">
              <arrow-down/>
            </el-icon>
          </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item v-for="(item, index) in projects" :key="index" :command="item">{{item.name}}</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
</template>

<script  setup lang="ts" name="customLayoutAside">
import { onMounted, ref } from "vue";
import { useBaseInfo } from '/@/stores/baseInfo';
import { storeToRefs } from "pinia";
import { Session } from '/@/utils/storage';


const { projects } = storeToRefs(useBaseInfo());

const getData = () => {
  useBaseInfo().setProjects();
};
const selectedProject = ref()
const handleDropdownCommand = (item: object) => {
  Session.set('selectedProject', item);
  selectedProject.value = item;
}


// 页面打开后获取列表数据
onMounted( async () => {
  getData();
  if (Session.get("selectedProject")){
    selectedProject.value = Session.get("selectedProject");
  };
});

</script>

<style scoped lang="scss">
.projectDropdownList {
  height: 30px;
  width: 100%;
  padding-bottom: 20px;
  padding-top: 20px;
  background-color: #85cf60;
  display: flex;
  align-items: center;
  justify-content: center;

  .el-dropdown {
    width: 100%;

    span {
      text-align: center;
      width: 100%;
      white-space: nowrap;
      display: inline-block;
      font-size: 18px;
    }
  }


}
.el-dropdown-menu {
    width: 200px;
    background-color: #85cf60;
  }
</style>
