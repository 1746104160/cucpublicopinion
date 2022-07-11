<template>
  <div class="center-cmp">
    <div class="cc-header">
      <dv-decoration-1 style="width:200px;height:50px;" />
      <div>新闻数据总数</div>
      <dv-decoration-1 style="width:200px;height:50px;" />
    </div>

    <div class="cc-details">
      <div class="card">
        2
      </div>
      <div class="card">
        1
      </div>
      <div class="card">
        3
      </div>
      <div class="card">
        7
      </div>
    </div>

    <div class="cc-main-container">
      <div class="ccmc-left">
        <div class="station-info">
          新华网<span>1315</span>
        </div>
        <div class="station-info">
          人民网<span>415</span>
        </div>
      </div>
      <div class="ccmc-middle">
        <div ref="wordcloudref" class="echart" />
      </div>
      <div class="ccmc-right">
        <div class="station-info">
          <span>90</span>光明网
        </div>
        <div class="station-info">
          <span>317</span>其他
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import { usewordcloud } from './usewordcloud'
export default defineComponent({
  name: 'CenterCmp',
  setup () {
    const wordcloudref = ref(undefined)
    onMounted(() => {
      usewordcloud(wordcloudref.value)
    })
    return {
      wordcloudref
    }
  }
})
</script>

<style lang="scss">
.center-cmp {
  width: 100%;
  height: 100%;
  margin: 0px;
  padding: 0px;
  display: flex;
  flex-direction: column;

  .cc-header {
    height: 70px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 30px;
  }

  .cc-details {
    height: 120px;
    display: flex;
    justify-content: center;
    font-size: 32px;
    align-items: center;

    .card {
      background-color: rgba(4, 49, 128, .6);
      color: #08e5ff;
      height: 70px;
      width: 70px;
      font-size: 45px;
      font-weight: bold;
      line-height: 70px;
      text-align: center;
      margin: 10px;
    }
  }

  .cc-main-container {
    position: relative;
    flex: 1;
    display: flex;

    .ccmc-middle {
      width: 60%;
      height: 90%;
      align-items: center;
      .echart{
        width: inherit;
        height: inherit;
        display: block;
        margin: 0 auto;
      }
    }

    .ccmc-left,
    .ccmc-right {
      width: 25%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      font-size: 24px;

      span {
        font-size: 40px;
        font-weight: bold;
      }

      .station-info {
        height: 80px;
        display: flex;
        align-items: center;
      }
    }

    .ccmc-left {
      align-items: flex-end;

      span {
        margin-left: 20px;
      }
    }

    .ccmc-right {
      align-items: flex-start;

      span {
        margin-right: 20px;
      }
    }
  }

  .label-tag {
    position: absolute;
    width: 500px;
    height: 30px;
    bottom: 10px;
    left: 50%;
    transform: translateX(-50%);
  }
}
</style>
