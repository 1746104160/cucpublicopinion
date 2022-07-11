<template>
  <div id="data-view">
    <dv-full-screen-container>
      <div class="main-header">
        <div class="mh-left">
          {{dataTime}}
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
          <Left-Chart-1 />
          <Left-Chart-2 />
          <Left-Chart-3 />
        </dv-border-box-3>

        <div class="right-main-container">
          <div class="rmc-top-container">
            <dv-border-box-3 class="rmctc-left-container">
              <Center-Cmp />
            </dv-border-box-3>

            <div class="rmctc-right-container">
              <dv-border-box-3 class="rmctc-chart-1">
                <Right-Chart-1 />
              </dv-border-box-3>

              <dv-border-box-4 class="rmctc-chart-2" :reverse="true">
                <Right-Chart-2 />
              </dv-border-box-4>
            </div>
          </div>

          <dv-border-box-4 class="rmc-bottom-container">
            <Bottom-Charts />
          </dv-border-box-4>
        </div>
      </dv-border-box-1>
    </dv-full-screen-container>
  </div>
</template>

<script lang="ts">
import { defineComponent, onBeforeMount, onMounted, ref } from 'vue'
import LeftChart1 from './components/LeftChart1.vue'
import LeftChart2 from './components/LeftChart2.vue'
import LeftChart3 from './components/LeftChart3.vue'
import CenterCmp from './components/CenterCmp.vue'
import RightChart1 from './components/RightChart1.vue'
import RightChart2 from './components/RightChart2.vue'
import BottomCharts from './components/BottomCharts.vue'
export default defineComponent({
  name: 'HomeDatav',
  components: {
    LeftChart1,
    LeftChart2,
    LeftChart3,
    CenterCmp,
    RightChart1,
    RightChart2,
    BottomCharts
  },
  setup () {
    let timer: NodeJS.Timer | null = null
    const dataTime = ref('')
    // 当前时间
    const getNowTime = () => {
      const now = new Date()
      const year = now.getFullYear()
      const month = now.getMonth() >= 9 ? now.getMonth() + 1 : `0${now.getMonth() + 1}`
      const date = now.getDate() >= 10 ? now.getDate() : `0${now.getDate()}`
      const hour = now.getHours() >= 10 ? now.getHours() : `0${now.getHours()}`
      const minutes = now.getMinutes() >= 10 ? now.getMinutes() : `0${now.getMinutes()}`
      const seconds = now.getSeconds() >= 10 ? now.getSeconds() : `0${now.getSeconds()}`
      dataTime.value = `${year}年${month}月${date}日 ${hour}:${minutes}:${seconds}`
    }
    const username = ref(JSON.parse(sessionStorage.getItem('userinfo') as string)?.name ?? '邵佳泓')
    onMounted(() => {
      getNowTime()
      timer = setInterval(() => {
        getNowTime()
      }, 1000)
    })
    onBeforeMount(() => {
      clearInterval(Number(timer))
    })
    return {
      username,
      dataTime
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

      a:visited {
        color: rgb(1, 134, 187);
      }
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

  .rmctc-chart-1,
  .rmctc-chart-2 {
    height: 50%;
  }
}
</style>
