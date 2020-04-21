<template>
    <div>
        <p>代码名称</p>
        <input v-model='name' placeholder='不超过32个字符' style="width: 600px;height: 30px;">

        <p align="center">代码编辑</p>
        <div style="width: 800pxl;height: 300px">
        <vue-editor v-model="message" :editor-toolbar="customToolbar"/>
        <!-- <textarea v-model='message' placeholder="多行文本输入……" align="center"></textarea> -->
        <!--v-model将标签的值与变量绑定-->
        </div>
        <span>保存</span>
        <input type="checkbox" v-model="save">
        <span>运行</span>
        <input type="checkbox" checked="checked"  v-model="run">
        <button @click="submit">提交</button>
        <button @click="test">测试</button>
        <!-- 以表格的形式展示查询得到的结果 -->
        <div v-bind:class="{ hide: active_hide_1}" align="left">
            <span>{{ head }}</span>
            <table>
                <thead>
                <tr>
                    <th v-for="th in tableTh" :key="th">
                        {{ th }}
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(col,index) in dataList" :key="index">
                    <td v-for="tr in tableTh" :key="tr">
                        {{col[tr]}}
                    </td>

                </tr>
                </tbody>
            </table>
            <button @click="showGraphSetting">显示可用的图形配置</button>
        </div>
        <!-- 以表格展示存放的图表配置 -->
        <div align="left" v-bind:class="{ hide: active_hide_2}">
            <span>可用图表配置</span>
            <table>
                <thead>
                <tr>
                    <th v-for="th in graphCols" :key="th">
                        {{ th }}
                    </th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(col,index) in graphTable" :key="index">
                    <td v-for="tr in graphCols" :key="tr">
                        {{col[tr]}}
                    </td>
                    <button @click="useSetting(index)">使用</button>

                </tr>
                </tbody>
            </table>
        </div>
        <div>
            <span style>图像标题</span>

            <input :value="chart_option.title.text" placeholder='不超过32个字符' style="width: 200px;height: 25px;"/>
            <span>标题字体</span>
            <select v-model="chart_option.title.textStyle.fontSize">
                <option v-for="val in [12,18,20,26]" :key="val" :value="val" v-text="val"></option>
            </select>
            <div>
                <span>备注</span>
                <input placeholder="请输入备注" v-model="graph_note"/>
            </div>
            <!-- 图表配置选项 -->
            <div>
                <div v-for="(series,index) in chart_option.series" :key="index">
                    <ul style="list-style-type:none">
                        <li>
                            <span>系列名称</span>
                            <input type="text" :value="series.name"/>
                        </li>
                        <li>
                            <span>x轴</span>
                            <select v-model="series.xAxis">
                                <option v-for="(th,index) in tableTh" :key="index" :value="th" v-text="th"></option>
                            </select>
                        </li>
                        <li>
                            <span>y轴</span>
                            <select v-model="series.yAxis">
                                <option v-for="(th,index) in tableTh" :key="index" :value="th" v-text="th"></option>
                            </select>
                        
                        </li>
                        <li>
                            <span>图表类型</span>
                            <select v-model="series.type">
                                <option v-for="(chart,index) in charts" :key="index" :value="chart.value" v-text="chart.type"></option>
                            </select>
                        
                        </li>
                        <li align="right">
                            <button @click="deleteSeries(index)">删除</button>
                        </li>

                    </ul>
                </div>
                <button @click="addSeries">添加系列</button>
            </div>
        </div>
        <div>

        </div>
        <button @click="drawLine()">显示图像</button>
        <button @click="saveGraph" :disabled="show_save_graph">保存图像配置</button>
        <div id="myChart" :style="{width:'600px', height:'400px'}"></div>
        <!-- <button @click="test">测试</button> -->



        
    </div>
    

</template>

<script>
import axios from 'axios';
import { VueEditor } from "vue2-editor";
export default{
    components: { VueEditor },
    data () {
        return {
            customToolbar:[['bold']],
            name: '',
            codeID:'',
            message: 'from app import engine\ncur = engine.connect()\nclass Query():\n\tdef solution(self):\n\t\treturn',
            head:'这是一个表',
            orderBy: ["c1","c2"],
            active_hide_1: true,
            active_hide_2: true,
            show_save_graph:true,
            graph_note:'',

            graphTable:{},
            graphCols:[],
            tableTh: [
                // 'item','sale'
                ],
            dataList: [
                // {item:'pans',sale:45},
                // {item:'jacket',sale:98},
                // {item:'shoes',sale:21},
            ],
            testOption : {
                title: { text: '在Vue中使用echarts'},
                tooltip: {},
                // xAxis: {
                    // data: ['衬衫','羊毛衫','雪纺衫','裤子','高跟鞋','袜子']
                    // data: [1,2,6,8,50,70]
                // },
                // yAxis: {},
                series: [{
                    name: '销量',
                    type: 'pie',
                    // data: [5,20,36,10,10,20]
                    // data:[
                    //     [1,1],[2,4],[3,9],[4,16],[5,25]
                       
                    // ]
                    data: [
                        {value:5,name:'衬衫'},
                        {value:20,name:'羊毛衫'},
                        {value:36,name:'雪纺衫'},
                        {value:10,name:'裤子'},
                        {value:10,name:'高跟鞋'},
                        {value:20,name:'袜子'},
                    ],
                }]
            },
            run:false,
            save:false,
            charts: [
                {
                    'type':'柱形图',
                    'value':'bar'

                },
                {
                    'type':'折线图',
                    'value':'line'
                },
                {
                    'type':'饼图',
                    'value':'pie'
                }
            ],
            chosen_chart:'',
            chartName:'',
            chart_option:{},
// 通用配置
            xAxis : {
                type:'category',

            },

            yAxis: {
                type: "value",
            },

            temp_chart_option: {
                title:{
                    textStyle: {
                        fontSize:18,
                        fontWeight: 'bolder',
                        color: "red"
                    
                    },
                    text:'这是一个图像',
                
                },
                tooltip : {},

                legend:{
                    data:[],
                },

                // color: [],//设置区分（每条线是什么颜色，和 legend 一一对应）

                series: [
                    {
                        name:'系列-1',

                        data:[],

                    },
                ],
                bar: {
                    barGap: '30%',            // 柱间距离，默认为柱形宽度的30%，可设固定值
                    barCategoryGap : '20%',   // 类目间柱形距离，默认为类目间距的20%，可设固定值

                },
                line: {
                    lineStyle: {
                        width: 2,
                        // type : 'solid'
                    },
                },

                pie: {
                    selectedOffset: 10,         // 选中是扇区偏移量
                },
            },

            current_option:{},



        }

    },
    created () {
        this.useDefaultOption()
        this.getMsg()
    },
    mounted () {
        // this.drawLine(this.testOption)
    },
    methods: {
        submit () {
            const path = 'http://127.0.0.1:5000/api/postCode';


            axios.post(path,{
                name: this.name,
                content: this.normalize(this.message),
                run:this.run,
                save:this.save,
                id: this.codeID,
            }).then(response => {
                console.log(response);
                if (response.data.type=='save') {};
                if (response.data.type=='run') {
                this.dataList = response.data.result;
                this.tableTh = Object.keys(response.data.result[0]);
                this.active_hide_1 = false;
                
                };
                alert(response.data.message);
            }).catch(function (error) {
                console.log(error)
                });

            
        },

        test () {
            // let a = '';
            // let b = [1,2,3,4];
            // let c = [];
            // b.forEach(element => {
            //     a = element+1
            //     c.push(a)
                
            // });
            // let c='';
            // c = this.is_all_number([1,2,6,4]);
            // console.log(c);
            console.log(this.current_option)
            if (JSON.stringify(this.current_option)!='{}') {
                console.log('is full')
                alert('is Full')
            }

            else {
                console.log('is empty')
                alert('is Empty')
            }

            

        },

        drawLine () {
            // 基于准备好的dom，初始胡echarts实例
            let option = this.modify_option()
            this.current_option = option
            // let option = Option
            let myChart  = this.$echarts.init(document.getElementById('myChart'))
            // 绘制图表

            myChart.setOption(this.current_option,true)
            this.show_save_graph=false
            
        },

        addSeries () {

            let series = this.chart_option.series
            let len = series.length
            let seriesName = '系列-' + (len+1)
            let blank =  {
                name : seriesName,
                type: '',
                xAxis: '',
                yAxis: '',
                data:[],
            };
            this.chart_option.series.push(blank)

        },

        deleteSeries(index) {
            this.chart_option.series.splice(index,1);

        },

        useDefaultOption () {
            this.chart_option = JSON.parse(JSON.stringify(this.temp_chart_option))
        },
// 组装思路：
//     默认模板不包括xAxis与yAxis属性，单独在data()里定义这两个对象，作为模板，不与任何元素属性绑定
//     在line与bar图形中拷贝这两个对象，并进一步设置并添加，pie不添加，因为他们的存在会画出坐标轴
//     x，y轴数据的选择通过series.data中把xAxis与yAxis属性设为表格中col值，在modify_option中
//     按图索骥，最后删除

        modify_option(op) {
            if (!op) {op = JSON.parse(JSON.stringify(this.chart_option))}
            // console.log(this.chart_option)
            
            op.series.forEach(element =>{
                    if (element.type=='pie') {
                        this.dataList.forEach(par =>{
                            let new_par= {};
                            new_par.name = par[element.xAxis];
                            new_par.value = par[element.yAxis];
                            element.data.push(new_par);

                        });
                    };
                        

                    if (element.type=='bar') {
                        op.xAxis = JSON.parse(JSON.stringify(this.xAxis))
                        op.yAxis = JSON.parse(JSON.stringify(this.yAxis))
                        op.xAxis.data = [];
                        this.dataList.forEach(par =>{
                            op.xAxis.data.push(par[element.xAxis]);
                            element.data.push(par[element.yAxis]);
                            // console.log(par[elment.xAxis]);
                        });
                    };

                    if (element.type=='line') {
                        op.xAxis = JSON.parse(JSON.stringify(this.xAxis))
                        op.yAxis = JSON.parse(JSON.stringify(this.yAxis))
                        let x_data= [];
                        this.dataList.forEach(par =>{
                            x_data.push(par[element.xAxis])
                        })
                        if (this.is_all_number(x_data)) {
                            op.xAxis.type = 'value';
                            this.dataList.forEach(par =>{
                                element.data.push(
                                    [par[element.xAxis],par[element.yAxis]]
                                    )
                            });

                        } else {
                            op.xAxis.data = [];
                            this.dataList.forEach(par =>{
                                op.xAxis.data.push(par[element.xAxis]);
                                element.data.push(par[element.yAxis]);
                            });
                        };
                    };

                    delete element.xAxis
                    delete element.yAxis
                    op.legend.data.push(element.name)
            })
            
            console.log('配置参数:',op);
            return op
        },

        is_all_number(arr) {
            let res = true;
            arr.forEach(ele =>{
                res = (typeof ele == 'number') && res;

            })
            return res
        },

        delete_data_from_setting (op) {
            op.series.forEach(ele => {
                ele.data.length = 0
                if (ele.type=='pie') {
                }

                if (ele.type=='line') {
                    if ('data' in op.xAxis) {
                        delete op.xAxis.data
                    }

                }
                if (ele.type=='bar') {
                    delete op.xAxis.data
                }
            })

            return op
            
        },
        saveGraph () {
            const path = 'http://127.0.0.1:5000/api/postGraph'
            if (JSON.stringify(this.current_option!='{}')) {
                let post_option = {}
                post_option = JSON.parse(JSON.stringify(this.current_option))
                let pure = {}
                pure =this.delete_data_from_setting(post_option)
                console.log('待储存的参数',pure)
                axios.post(path,{
                    'setting':pure,
                    'note':this.graph_note
                }).then(response => {
                    console.log('执行保存图片获得的反馈：',response)
                }).catch(error => {
                    console.log(error)
                })
            }
            else {
                alert('Graph Setting is empty!')
            }

                


        },

        removeArray (arr, val) {
            for(var i = 0; i < arr.length; i++) {

                if(arr[i] == val) {
                    arr.splice(i, 1);
                    break;
                }
            }

        },

        showGraphSetting () {
            const path = 'http://127.0.0.1:5000/api/getdata'
            axios.post(path,{
                db:'rest',
                table:'graphsetting'
            }).then(response => {
                console.log(response)
                this.graphTable = response.data.jsonData.main
                this.graphCols = response.data.jsonData.columns
                this.removeArray(this.graphCols,'setting')
                this.active_hide_2 = false

            })
        },

        empty_obj (obj) {
            Object.keys(obj).forEach(ele =>{
                delete obj[ele]
            })
        },
        useSetting (index) {

            this.chart_option = JSON.parse(JSON.stringify(this.graphTable[index].setting))




        },

        getMsg() {

            console.log(this.$router)
            let msg = this.$router.history.current.query
            let firstCols = ''
            if (JSON.stringify(msg)!='{}') {
                console.log(JSON.stringify(msg)!='{}')
                // this.messgae.length = 0
                this.message = this.htmlize(msg.Content.content)
                // this.message = msg.Content.content
                this.name  = msg.Content.name
                // firstCols = Object.keys(msg.Content)[0]
                // this.codeID = msg.Content[firstCols]
                this.codeID = msg.Content.id
            }

            
        },

        normalize (content) {
            console.log(content)
            let res = content.replace(/<p>/g,'').replace(/<\/p>/g,'\n')
            // 从html中读取时需要转换这个敏感字符，但是给段落加标签反而不用逆转换
            res = res
            .replace(/&lt;/g, "<")
            .replace(/&gt;/g, ">")
            .replace(/&quot;/g, "\"")
            .replace(/&#39;/g, "\'")

            console.log(res)
            return res

        },

        htmlize (content) {
            let arr = content.split('\n')
            console.log(arr)
            let res = ''
            arr.forEach(ele => {
                console.log(ele)
                res = res + "<p>" + ele + "</p>"
            })
            console.log(res)
            return res
        },


    }
}

</script>