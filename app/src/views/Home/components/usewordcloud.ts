/*
 * @Descripttion: 业务管理系统
 * @version: 1.0.0
 * @Author: 邵佳泓
 * @Date: 2022-07-10 15:36:54
 * @LastEditors: 邵佳泓
 * @LastEditTime: 2022-07-10 16:13:53
 * @FilePath: /app/src/views/Home/components/usewordcloud.ts
 */
import * as echarts from 'echarts'
import 'echarts-wordcloud'
export const usewordcloud = (chartDom: HTMLElement | undefined) => {
  const mychart = echarts.init(chartDom as HTMLElement)
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
      data: [
        {
          name: '新浪网',
          value: 6181,
          url: 'https://news.sina.com.cn/'
        },
        {
          name: '搜狐新闻',
          value: 4386,
          url: 'https://www.sohu.com/'
        },
        {
          name: '人民日报',
          value: 4055,
          url: 'http://www.people.com.cn/'
        },
        {
          name: '光明日报',
          value: 2467,
          url: 'https://epaper.gmw.cn/'
        },
        {
          name: '新华网',
          value: 2244,
          url: 'http://news.cn/'
        },
        {
          name: '央视新闻',
          value: 1898,
          url: 'https://news.cctv.com/'
        },
        {
          name: '经济日报',
          value: 1484,
          url: 'http://paper.ce.cn/'
        }]
    }]
  }
  mychart.setOption(option)
  mychart.on('click', function (params:any) {
    window.open(params.data.url!, 'target')
  })
  option && mychart.setOption(option)
}
export default { usewordcloud }
