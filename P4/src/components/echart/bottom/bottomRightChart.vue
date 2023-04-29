<template>
  <div>
    <div id="bottomRightChart" style="width:13rem;height:5.5rem;"></div>
  </div>
</template>

<script>
import echartMixins from "@/utils/resizeMixins";
import data from 'C:/Users/12979/Desktop/share/test.json'
export default {
  data() {
    return {
      chart: null,
      jsonData:data
    };
  },
  mounted() {
    this.draw();
  },
  mixins: [echartMixins],
  methods: {
    draw() {
      // 基于准备好的dom，初始化echarts实例
      this.chart = this.$echarts.init(document.getElementById("bottomRightChart"));
      let option = {
        tooltip: {
    trigger: 'item',
    triggerOn: 'mousemove',
  },
  animation: false,
  legend: {
    top: '10%',
    left: 'center',
    textStyle:{ color:[]}
  },
  series: [
    {
      type: 'sankey',
      bottom: '10%',
      emphasis: {
        focus: 'adjacency'
      },
      data: [
        { name: 's1-s2' ,itemStyle:{color:"#76FF03"}},
        { name: 's2-s1' ,itemStyle:{color:"#00C853"} },
        { name: 's2-s3' ,itemStyle:{color:"#18FFFF"}},
        { name: 's3-s2' ,itemStyle:{color:"#1DE9B6"}},
        { name: 's1-s3' ,itemStyle:{color:"#EEFF41"}},
        { name: 's3-s1' ,itemStyle:{color:"#AEEA00"}},
        { name: '字节数(KB)' ,itemStyle:{color:"#FFCC80"}},
        { name: '包数' ,itemStyle:{color:"#FB8C00"}},
      ],
      links: [
        { source: 's1-s2', target: '字节数(KB)',value:this.jsonData[1]["counter.data.byte_count"]/1000},
        { source: 's2-s1', target: '字节数(KB)',value:this.jsonData[3]["counter.data.byte_count"]/1000},
        { source: 's2-s3', target: '字节数(KB)',value:this.jsonData[5]["counter.data.byte_count"]/1000},
        { source: 's3-s2', target: '字节数(KB)',value:this.jsonData[7]["counter.data.byte_count"]/1000},
        { source: 's1-s3', target: '字节数(KB)',value:this.jsonData[9]["counter.data.byte_count"]/1000},
        { source: 's3-s1', target: '字节数(KB)',value:this.jsonData[11]["counter.data.byte_count"]/1000},
        
        { source: 's1-s2', target: '包数',value:this.jsonData[1]["counter.data.packet_count"]  },
        { source: 's2-s1', target: '包数',value:this.jsonData[3]["counter.data.packet_count"]  },
        { source: 's2-s3', target: '包数',value:this.jsonData[5]["counter.data.packet_count"]  },
        { source: 's3-s2', target: '包数',value:this.jsonData[7]["counter.data.packet_count"]  },
        { source: 's1-s3', target: '包数',value:this.jsonData[9]["counter.data.packet_count"]  },
        { source: 's3-s1', target: '包数',value:this.jsonData[11]["counter.data.packet_count"] }
      ],
    
      label: {
        position: 'right',
        color:'source'
      },
      lineStyle: {
        color: 'target',
        curveness: 0.5
      }
    }
  ]};

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