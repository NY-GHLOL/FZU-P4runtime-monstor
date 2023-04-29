<template>
  <div>
    <div id="bottomLeftChart2" style="width:8rem;height:5rem;"></div>
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
    this.draw2();
  },
  methods: {
    draw2(){
      this.chart = this.$echarts.init(document.getElementById("bottomLeftChart2"));
      let option2 = {  
        tooltip: {
    trigger: 'item'
  },
  legend: {
    top: '3%',
    left: 'center',
    textStyle:{ color:[]}
  },
  color:['#F44336','#FF8A65','#FFF176'],
  series: [
    {
      name: 'Packet_count',
      type: 'pie',
      center:['70%','50%'],
      radius: ['50%', '70%'],
      avoidLabelOverlap: false,
      label: {
        show: false,
        position: 'center'
      },
      emphasis: {
        label: {
          show: true,
          fontSize: 20,
          fontWeight: 'bold',
        }
      },
      labelLine: {
        show: false
      },
      data: [
        { value: this.jsonData["1"]["counter.data.packet_count"], name: 's1-s2' },
        { value: this.jsonData["9"]["counter.data.packet_count"], name: 's2-s3' },
        { value: this.jsonData["5"]["counter.data.packet_count"], name: 's1-s3' },
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

