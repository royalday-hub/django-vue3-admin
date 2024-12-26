<template>
  <div class="card-wrap">
    <el-card
        v-if="showAdd"
        shadow="hover"
        class="box-card card-add"
        @click.native="add()"
    >
      <div class="card-add-content">
        <i class="el-icon-circle-plus-outline"/>
      </div>
    </el-card>
    <el-card
        :shadow="item.active ? 'always' : 'hover'"
        :class="['box-card', { active: item.active }]"
        v-for="item in cardList"
        :key="item.id"
        @click.native="selectCard($event, item)"
    >
      <div :class="['card-status', item.type]" style="right:230px;"></div>
      <div class="card-header">
        <img height="66px" :src="'./image/icon/'+ item.typeDESC +'.png'"/>
        <div class="header-text">
          <div :title="item.name" class="title">{{ item.name }}</div>
          <span :title="item.description">{{ item.description }}</span>
        </div>
      </div>
      <div class="card-content">
        <span>负责人:</span>
        {{ item.creator_name }}
      </div>
      <div class="card-content">
        <span>用例数:</span>
        {{ item.count }}
      </div>
      <br/>
      <div class="card-content" style="width: 100%;">
        <span>关联节点:</span>
        {{ item.nodeName }}
        <a @click="operate('setNode', item)" style="float: right;font-size: 12px;color: blue;">去关联</a>
      </div>
      <div :class="['card-footer', {'card-result-footer': type === 'result'}]">
        <!-- 这里你去根据 type=node 去判断下节点管理里的操作按钮 -->
        <div v-if="type === 'result'">
          <icon-button
              icon="el-icon-view"
              title="查看详细结果"
              style="margin-left: 15px"
              @click.native="operate('view', item)"
          />
        </div>
        <template v-else>
          <icon-button
              icon="el-icon-edit"
              tips="编辑"
              @click.stop.native="operate('edit', item)"
          />
          <icon-button
              icon="el-icon-delete"
              tips="删除"
              @click.stop.native="operate('delete', item)"
          />
          <icon-button
              icon="el-icon-s-promotion"
              tips="运行"
              @click.stop.native="operate('run', item)"
          />
          <icon-button
              icon="el-icon-edit-outline"
              tips="编辑详细用例"
              @click.stop.native="operate('editDetail', item)"
          />
        </template>
      </div>
    </el-card>
  </div>
</template>

<script lang="ts" setup name="GroupCard">
import {ref, onMounted} from 'vue';
import IconButton from "/@/components/IconButton/index.vue";
import * as api from './api';

interface cardType {
  active: boolean
  name: string
  description: string
  creator_name: string
  count: number
  nodeName: string
}

let cardList: cardType[] = [];

let props = defineProps(["showAdd", "type"])
let $emit = defineEmits(["handlerAdd", "handlerSelect", "handlerOperate"])


// 页面加载时，调用获取项目接口
const getGroupInfo = () => {
  api.GetList({}).then((res: { data: { data: never[]; }; }) => {
    cardList = res.data.data;
    if (cardList.length > 0) {
      (cardList as { active: boolean }[])[0].active = true;
    }
  }).catch((e: any) => {
    console.log(e);
  });
}

const add = () => {
  $emit("handlerAdd");
};

const selectCard = ($event: { target: { className: string | string[]; }; }, item: cardType) => {
  if ($event.target.className.indexOf("icon-item") === -1) {
    cardList.forEach((item) => {
      item.active = false;
    });
    item.active = true;
    cardList = [...cardList];
    $emit("handlerSelect", item);
  }
};
const operate = (type: any, item: cardType) => {
  $emit("handlerOperate", {type, item});
}
onMounted(() => {
  getGroupInfo();
});


</script>

<style lang="scss" scoped>
.card-wrap {
  background-color: #ffffff;
  overflow-y: auto;
  padding: 8px;
  height: 100%;

  .box-card {
    width: 280px;
    display: inline-block;
    margin-right: 16px;
    position: relative;

    &.active {
      background-color: rgb(217, 236, 255);
    }

    &.card-add {
      height: 175px;
      cursor: pointer;

      &:hover {
        background: rgba(0, 0, 0, 0.025);
      }

      .card-add-content {
        height: 135px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        color: #5a5e66;

        i {
          font-size: 36px;
        }
      }
    }

    .card-status {
      width: 46px;
      height: 20px;
      line-height: 20px;
      position: absolute;
      top: 0px;
      right: 0px;
      font-size: 12px;
      text-align: center;
      color: white;

      &.pass {
        background-color: #67c23a;

        &::before {
          content: "通过";
        }
      }

      &.fail {
        background-color: #f56c6c;

        &::before {
          content: "失败";
        }
      }

      &.NA {
        background-color: #e6a23c;

        &::before {
          content: "未运行";
        }
      }

      &.Web {
        background-color: #67c23a;

        &::before {
          content: "Web";
        }
      }

      &.Inter {
        background-color: #00aaff;

        &::before {
          content: "接口";
        }
      }

    }

    .card-header {
      height: 60px;
      margin-bottom: 7px;

      img {
        float: left;
      }

      .header-text {
        margin-left: 80px;
        font-size: 12px;
        color: #909399;

        .title {
          color: #303133;
          font-size: 15px;
          font-weight: bold;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          line-height: 20px;
          margin-bottom: 8px;
        }

        span {
          overflow: hidden;
          text-overflow: ellipsis;
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          line-height: 16px;
          white-space: normal;
        }
      }
    }

    .card-content {
      width: 50%;
      display: inline-block;
      font-size: 14px;
      font-weight: 500;
      color: #606266;

      span {
        font-size: 12px;
        color: #909399;
        font-weight: normal;
      }
    }

    .card-footer {
      margin: 7px -20px -20px;
      height: 60px;
      background-color: #f1f4f7;
      display: flex;
      align-items: center;
      justify-content: space-around;
    }

    .card-result-footer {
      justify-content: unset;
    }
  }
}
</style>
