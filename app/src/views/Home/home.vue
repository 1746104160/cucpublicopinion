<template>
  <div id="data-view">
    <dv-full-screen-container>
      <div class="main-header">
        <div class="mh-left">
          <dv-digital-flop :config="dataTime" style="height: 80px;" />
        </div>
        <div class="mh-middle">
          新闻舆情分析
        </div>
        <div class="mh-right">
          <dv-border-box-2 style="width: 120px; height: 50px; line-height: 50px; text-align:center;margin-left:200px;">
            {{ username }}
          </dv-border-box-2>
        </div>
      </div>

      <dv-border-box-1 class="main">
        <dv-border-box-3 class="left-chart-container">
          <Left-Chart-1 :sentiments="sentiments" />
          <Left-Chart-2 :categories="categories" />
        </dv-border-box-3>

        <div class="right-main-container">
          <div class="rmc-top-container">
            <dv-border-box-11 class="rmctc-left-container" :title="'新闻数据总数'">
              <Center-Cmp :total="total" :datas="postnums" />
            </dv-border-box-11>

            <div class="rmctc-right-container">
              <dv-border-box-9 class="rmctc-chart">
                <Right-Chart :clusters="clusters" />
              </dv-border-box-9>
            </div>
          </div>

          <dv-border-box-4 class="rmc-bottom-container">
            <Bottom-Charts :config1="config1" :config2="config2" :config3="config3" :config4="config4" :title1="title1" :title2="title2" :title3="title3" :title4="title4"/>
          </dv-border-box-4>
        </div>
      </dv-border-box-1>
    </dv-full-screen-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, onMounted, reactive, ref } from 'vue'
import LeftChart1 from './components/LeftChart1.vue'
import LeftChart2 from './components/LeftChart2.vue'
import CenterCmp from './components/CenterCmp.vue'
import RightChart from './components/RightChart.vue'
import BottomCharts from './components/BottomCharts.vue'
import Service from './api/index'
export default defineComponent({
  name: 'HomeDatav',
  components: {
    LeftChart1,
    LeftChart2,
    CenterCmp,
    RightChart,
    BottomCharts
  },
  setup () {
    const total = ref('')
    const postnums = ref([{ name: '', value: 0 }, { name: '', value: 0 }, { name: '', value: 0 }, { name: '', value: 0 }])
    const categories = ref([{ name: '', value: 0 }])
    const sentiments = ref([{ name: '', value: 0 }])
    const clusters = ref([{ name: '', value: 0 }])
    const config1 = ref([{ name: '', value: 0 }])
    const config2 = ref([{ name: '', value: 0 }])
    const config3 = ref([{ name: '', value: 0 }])
    const config4 = ref([{ name: '', value: 0 }])
    const title1 = ref('')
    const title2 = ref('')
    const title3 = ref('')
    const title4 = ref('')
    let timer: NodeJS.Timer | null = null
    const formatter = (number: number) => {
      if (number < 10) {
        return '0' + number
      } else {
        return number.toString()
      }
    }
    const dataTime = reactive({
      number: [0, 0, 0, 0, 0, 0],
      content: '{nt}年{nt}月{nt}日 {nt}:{nt}:{nt}',
      formatter
    })
    // 当前时间
    const getNowTime = () => {
      const now = new Date()
      dataTime.number[0] = now.getFullYear()
      dataTime.number[1] = now.getMonth() + 1
      dataTime.number[2] = now.getDate()
      dataTime.number[3] = now.getHours()
      dataTime.number[4] = now.getMinutes()
      dataTime.number[5] = now.getSeconds()
    }
    const username = ref(JSON.parse(sessionStorage.getItem('userinfo') as string)?.name ?? '邵佳泓')
    onMounted(() => {
      getNowTime()
      Service.getPostnum().then((res: any) => {
        total.value = res.data.total.toString()
        postnums.value = res.data.data
        Service.getSentimentforarticleSource(postnums.value[0].name).then((res: any) => {
          config1.value = res.data
          title1.value = postnums.value[0].name
        })
        Service.getSentimentforarticleSource(postnums.value[1].name).then((res: any) => {
          config2.value = res.data
          title2.value = postnums.value[1].name
        })
        Service.getSentimentforarticleSource(postnums.value[2].name).then((res: any) => {
          config3.value = res.data
          title3.value = postnums.value[2].name
        })
        Service.getSentimentforarticleSource(postnums.value[3].name).then((res: any) => {
          config4.value = res.data
          title4.value = postnums.value[3].name
        })
      })
      Service.getCategory().then((res: any) => {
        categories.value = res.data
      })
      Service.getSentiment().then((res: any) => {
        sentiments.value = res.data
      })
      Service.getCluster().then((res: any) => {
        clusters.value = res.data
      })
      timer = setInterval(() => {
        getNowTime()
      }, 1000)
    })
    onBeforeMount(() => {
      clearInterval(Number(timer))
    })
    return {
      username,
      dataTime,
      total,
      postnums,
      categories,
      sentiments,
      clusters,
      config1,
      config2,
      config3,
      config4,
      title1,
      title2,
      title3,
      title4
    }
  }
})
</script>

<style lang="scss">
#data-view {
  position: relative;
  background-color: #030409;
  color: #fff;
  width: 100%;
  height: 100%;
  overflow-x: hidden;

  #dv-full-screen-container {
    position: relative;
    max-width: calc(100vw) !important;
    max-height: calc(100vh) !important;
    background-image: url('@/assets/bg.png');
    background-size: 99% 99%;
    box-shadow: 0 0 3px blue;
    display: flex;
    flex-direction: column;
  }

  .main-header {
    height: 80px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;

    .mh-left {
      font-size: 20px;
      color: rgb(1, 134, 187);
    }

    .mh-middle {
      font-size: 30px;
    }

    .mh-left,
    .mh-right {
      width: 450px;
    }
  }

  .main {
    padding: 10px;
    height: calc(100vh - 80px);

    .border-box-content {
      padding: 20px;
      box-sizing: border-box;
      display: flex;
    }
  }

  .left-chart-container {
    width: 22%;
    padding: 10px;
    box-sizing: border-box;

    .border-box-content {
      flex-direction: column;
    }
  }

  .right-main-container {
    width: 78%;
    padding-left: 5px;
    box-sizing: border-box;
  }

  .rmc-top-container {
    height: 65%;
    display: flex;
  }

  .rmctc-left-container {
    width: 65%;
  }

  .rmctc-right-container {
    width: 35%;
  }

  .rmc-bottom-container {
    height: 35%;
  }

  .rmctc-chart {
    height: 100%;
  }
}
</style>
