<template>
  <div>
    <div id="bottomLeftChart" style="width:5rem;height:4rem;"></div>
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
      this.chart = this.$echarts.init(document.getElementById("bottomLeftChart"));
      //  ----------------------------------------------------------------
      let option = {
          title: {
        },
        tooltip: {},
        animationDurationUpdate: 1500,
        animationEasingUpdate: 'quinticInOut',
        series: [
          {
            type: 'graph',
            layout: 'none',
            symbolSize: 50,
            roam: true,
            label: {
              show: true
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [5, 10],
            edgeLabel: {
              fontSize:11
            },
            data: [
              {
                name: 'S1',
                x: 300,
                y: 300
              },
              {
                name: 'S2',
                x: 800,
                y: 300
              },
              {
                name: 'S3',
                x: 550,
                y: 0
              },
            ],
            // links: [],
            links: [
              {
                source: 'S1',
                target: 'S2',
                symbolSize: [5, 10],
                label: {
                  show: true,
                  formatter: 'S1>S2 tunnel-100'
                },
                lineStyle: {
                  curveness: 0.2,
                  color:'#76FF03'
                }
              },
              {
                source: 'S2',
                target: 'S1',
                label: {
                  show: true,
                  formatter: 'S2>S1 tunnel-200'
                },
                lineStyle: {
                  curveness: 0.2,
                  color:'#00C853'
                }
              },
              {
                source: 'S1',
                target: 'S3',
                label: {
                  show: true,
                  formatter: 'S1>S3 tunnel-300'
                },
                lineStyle: {
                  curveness: 0.2,
                  color:'#EEFF41'
                }
              },
              {
                source: 'S3',
                target: 'S1',
                label: {
                  show: true,
                  formatter: 'S3>S1 tunnel-400'
                },
                lineStyle: {
                  curveness: 0.2,
                  color:'#AEEA00'
                }
              },
              {
                source: 'S2',
                target: 'S3',
                label: {
                  show: true,
                  formatter: 'S2>S3 tunnel-500'
                },
                lineStyle: {
                  curveness: 0.2,
                  color: '#18FFFF'
                }
              },
              {
                source: 'S3',
                target: 'S2',
                label: {
                  show: true,
                  formatter: 'S3>S2 tunnel-600'
                },
                lineStyle: {
                  curveness: 0.2,
                  color: '#1DE9B6'
                }
              },
            ],
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0
            }
          }
        ]
    };

    
      this.chart.setOption(option);
    }
  },
  destroyed() {
    window.onresize = null;
  }
};
</script>

<style lang="scss" scoped>
</style>
