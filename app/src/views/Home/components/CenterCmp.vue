<template>
  <div class="center-cmp">

    <div class="cc-details">
      <div v-for="digit in total" :key="digit" class="card">
        {{ digit }}
      </div>
    </div>

    <div class="cc-main-container">
      <div class="ccmc-left">
        <div v-for="data of datas.slice(0,2)" :key="data" class="station-info">
          {{ data.name }}<span>{{ data.value }}</span>
        </div>
      </div>
      <div class="ccmc-middle">
        <div ref="wordcloudref" class="echart" />
      </div>
      <div class="ccmc-right">
        <div v-for="data of datas.slice(2,4)" :key="data" class="station-info">
          <span>{{ data.value }}</span>{{ data.name }}
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue'
import { usewordcloud } from './usewordcloud'
import Service from '../api'
import { useRouter } from 'vue-router'
export default defineComponent({
  name: 'CenterCmp',
  props: {
    total: {
      type: String,
      default: ''
    },
    datas: {
      default: () => { return [{ name: '', value: 0 }, { name: '', value: 0 }, { name: '', value: 0 }, { name: '', value: 0 }] as any[] }
    }
  },
  setup (props) {
    const router = useRouter()
    const wordcloudref = ref(undefined)
    onMounted(() => {
      Service.getHotword().then((res:any) => {
        const data = [] as any[]
        res.data.forEach((element:any) => {
          data.push({
            name: element.hot_word,
            value: element.hot
          })
        })
        usewordcloud(wordcloudref.value, data, router)
      })
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

  .cc-details {
    height: 120px;
    padding-top: 50px;
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
      width: 80%;
      height: 100%;
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
