<template>
  <div>
    <div id="right" style="width:8rem;height:5rem;"></div>
  </div>
</template>

<script>
import echartMixins from "@/utils/resizeMixins";
import data from './test2.json'
export default {
  data() {
    
    return {
      chart: null,
      jsonData:data
    };
  },
  mixins: [echartMixins],
  mounted() {
    this.draw();
  },
  methods: {
    draw() {
      // 基于准备好的dom，初始化echarts实例
      this.chart = this.$echarts.init(document.getElementById("right"));
      //  ----------------------------------------------------------------
      
      // let category = [this.jsonData["1"]["sw.name"],this.jsonData["2"]["sw.name"],this.jsonData["3"]["sw.name"],this.jsonData["4"]["sw.name"]];
      // let lineData = [
      // this.jsonData["1"]["index"],
      // this.jsonData["2"]["index"],
      // this.jsonData["3"]["index"],
      // this.jsonData["4"]["index"],];
      // let barData = [];
      // let rateData = [];
      // for (let i = 0; i < 33; i++) {
      //   let rate = barData[i] / lineData[i];
      //   rateData[i] = rate.toFixed(2);
      // }

      let option = {
        // title: {
        //   text: "",
        //   x: "center",
        //   y: 0,
        //   textStyle: {
        //     color: "#B4B4B4",
        //     fontSize: 16,
        //     fontWeight: "normal"
        //   }
        // },
        // tooltip: {
        //   trigger: "axis",
        //   backgroundColor: "rgba(255,255,255,0.1)",
        //   axisPointer: {
        //     type: "shadow",
        //     label: {
        //       show: true,
        //       backgroundColor: "#7B7DDC"
        //     }
        //   }
        // },
        // legend: {
        //   data: ["已贯通", "计划贯通", "贯通率"],
        //   textStyle: {
        //     color: "#B4B4B4"
        //   },
        //   top: "0%"
        // },
        // grid: {
        //   x: "8%",
        //   width: "88%",
        //   y: "4%"
        // },
        // xAxis: {
        //   data: category,
        //   axisLine: {
        //     lineStyle: {
        //       color: "#B4B4B4"
        //     }
        //   },
        //   axisTick: {
        //     show: false
        //   }
        // },
        // yAxis: [
        //   {
        //     splitLine: { show: false },
        //     axisLine: {
        //       lineStyle: {
        //         color: "#B4B4B4"
        //       }
        //     },

        //     axisLabel: {
        //       formatter: "{value} "
        //     }
        //   },
        //   {
        //     splitLine: { show: false },
        //     axisLine: {
        //       lineStyle: {
        //         color: "#B4B4B4"
        //       }
        //     },
        //     axisLabel: {
        //       formatter: "{value} "
        //     }
        //   }
        // ],
        // series: [
        //   {
        //     name: "贯通率",
        //     type: "line",
        //     smooth: true,
        //     showAllSymbol: true,
        //     symbol: "emptyCircle",
        //     symbolSize: 8,
        //     yAxisIndex: 1,
        //     itemStyle: {
        //       normal: {
        //         color: "#F02FC2"
        //       }
        //     },
        //     data: rateData
        //   },

        //   {
        //     name: "已贯通",
        //     type: "bar",
        //     barWidth: 10,
        //     itemStyle: {
        //       normal: {
        //         barBorderRadius: 5,
        //         color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
        //           { offset: 0, color: "#956FD4" },
        //           { offset: 1, color: "#3EACE5" }
        //         ])
        //       }
        //     },
        //     data: barData
        //   },

        //   {
        //     name: "计划贯通",
        //     type: "bar",
        //     barGap: "-100%",
        //     barWidth: 10,
        //     itemStyle: {
        //       normal: {
        //         barBorderRadius: 5,
        //         color: new this.$echarts.graphic.LinearGradient(0, 0, 0, 1, [
        //           { offset: 0, color: "rgba(156,107,211,0.8)" },
        //           { offset: 0.2, color: "rgba(156,107,211,0.5)" },
        //           { offset: 1, color: "rgba(156,107,211,0.2)" }
        //         ])
        //       }
        //     },
        //     z: -12,

        //     data: lineData
        //   }
        // ]
  tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '3%',
    left: 'center'
  },
  color:['#B71C1C','#6A1B9A','#CDDC39'

  ],
  series: [
    {
      name: 'Byte_count',
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'left'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 40,
          fontWeight: 'bold',
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: this.jsonData["1"]["counter.data.byte_count"], name: 's1-s2' },
        { value: this.jsonData["9"]["counter.data.byte_count"], name: 's2-s3' },
        { value: this.jsonData["5"]["counter.data.byte_count"], name: 's1-s3' },
        // { value: 484, name: 'Union Ads' },
        // { value: 300, name: 'Video Ads' }
      ]
    }
  ]
      };
      this.chart.setOption(option);
    },
    draw2(){
      this.chart = this.$echarts.init(document.getElementById("right"));
      let option2 = {  
        tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '3%',
    left: 'center'
  },
  color:['#B71C1C','#6A1B9A','#CDDC39'

  ],
  series: [
    {
      name: 'Byte_count',
      type: 'pie',
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 50,
          fontWeight: 'bold',
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: this.jsonData["1"]["counter.data.byte_count"], name: 's2-s2' },
        { value: this.jsonData["9"]["counter.data.byte_count"], name: 's3-s3' },
        { value: this.jsonData["5"]["counter.data.byte_count"], name: 's1-s1' },
        // { value: 484, name: 'Union Ads' },
        // { value: 300, name: 'Video Ads' }
      ]
    }
  ]
      };
      this.chart.setOption(option2);
    }
  },
  destroyed() {
    window.onresize = null;
  }
};
</script>

<style lang="scss" scoped>
</style>


<!-- import * as echarts from 'echarts'; -->

<!-- var chartDom = document.getElementById('main');
var myChart = echarts.init(chartDom);
var option; -->

