<template>
    <div :id="uuid" :style="style"></div>
</template>

<script setup lang="ts">
    import {watch, ref, computed, onMounted} from 'vue'
    import * as Echarts from 'echarts'
    import _ from 'lodash'

    let Props = defineProps({
        height: {
            type: String,
            default: '400px'
        },
        width: {
            type: String,
            default: '600px'
        },

        options: {
            type: Object,
            default: null
        }
    });
    let uuid: any = null;
    let myChart: any = null;

    const idGen = () => {
        return new Date().getTime()
    };

    let needWidth = ref(Props.width);
    let mYOptions = ref(Props.options);
    let style: any = {};

    watch(needWidth, (newValue, oldValue) => {
        // 防抖后执行的操作
        if (myChart) {
            setTimeout(() => {
                myChart.resize({
                    //过渡动画时长
                    animation: {
                        duration: 300
                    }
                })
            }, 0);
        }
    });
    computed(() => {
        style = () => {
            return {
                height: Props.height,
                width: Props.width
            }
        }
    });
    onMounted(() => {
        uuid = idGen();
        // 准备实例
        myChart = Echarts.init((document.getElementById(uuid) as HTMLElement));
        // 应用配置项
        mYOptions.value.deep = true;
        myChart.setOption(mYOptions.value, {notMerge: true});
    });

</script>

<style scoped>

</style>
