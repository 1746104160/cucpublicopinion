/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 15:36:54
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-13 20:32:55
 * @FilePath: /app/src/views/Home/components/usewordcloud.ts
 */
import * as echarts from 'echarts'
import 'echarts-wordcloud'

export const usewordcloud = (chartDom: HTMLElement | undefined, data:any[], router:any) => {
  const option = {
    tooltip: {},
    series: [{
      type: 'wordCloud',
      gridSize: 2,
      sizeRange: [12, 50],
      rotationRange: [-90, 90],
      shape: 'pentagon',
      drawOutOfBound: true,
      textStyle: {
        color: function () {
          return 'rgb(' + [
            Math.round(100 + Math.random() * 155),
            Math.round(100 + Math.random() * 155),
            Math.round(100 + Math.random() * 155)
          ].join(',') + ')'
        }
      },
      emphasis: {
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data
    }]
  }
  const mychart = echarts.init(chartDom as HTMLElement)
  mychart.setOption(option)
  mychart.on('click', function (params:any) {
    router.push({ name: 'newsManage', params: { keyword: params.data.name } })
  })
  option && mychart.setOption(option)
}
export default { usewordcloud }
