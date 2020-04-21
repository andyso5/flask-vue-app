
<template>
<!-- vue文件里不能设置style，但是可以再index.html里设置 -->
    <div align="left">
        <div>
        <select v-model="db_index" >
            <option v-for="(datebase,index) in jsonData" :key="index" :value="index+1">{{ datebase.db }}</option>
        </select>

        <select v-if="db_index" v-model="tb">
            <option v-for="table in jsonData[db_index-1].tables" :key="table" :value="table">{{ table }}</option>

        </select>
        <button @click="postquery">查询</button>
        </div>

    
        <!-- <button @click="getdata">GetData</button> -->
        <p align="left">{{ head }}</p>
        <table>
            <thead>
            <tr>
                <!-- <th v-bind:class="{ hide: active_hide}">序号</th> -->
                <th v-for="th in tableTh" :key="th">
                    {{ th }}
                </th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="(col,index) in dataList" :key="index">


                <td v-for="tr in tableTh" :key="tr">
                    {{col[tr]}}
                    <!-- {{col.th}} -->
                </td>

            </tr>
            </tbody>
        </table> 

        <!-- <div id="myChart" :style="{width:'600px', height:'400px'}"></div>        -->
    </div>

</template>


<script>
import axios from 'axios'

export default{

    data () {
        return {
            db_index: null,
            tb: null,
            jsonData:[
                {
                    'db':'res',
                    'tables':['data','table']
                    // 'data':['id','name','ps'],
                    // 'table':['id','stu','score']
                    },
                {
                    'db':'mysql',
                    'tables':['info'],
                    },
            ],

            head:'这是一个表',
            orderBy: ["c1","c2"],
            active_hide: true,
            tableTh: [
                ],
            dataList: [
                // {
                //     'name': 'xiaoao',
                //     'content': 'apple'
                // },
                // {
                //     'name':'jianghan',
                //     'content': 'tomato'
                // }
                ],
            


        }
    },
    mounted () {
        // this.drawLine();
    },
    created () {
        this.getTables()
    },

    methods: {
        getdata () {
            const path = 'http://127.0.0.1:5000/api/getdata';
            axios.get(path).then(response => {
                this.dataList = response.data
                this.tableTh = Object.keys(response.data[0])
                this.active_hide = false
            }).catch(error => {
                console.log(error)
            })
        },

        getTables () {
            const path = 'http://127.0.0.1:5000/api/gettb';

            axios.get(path).then(response => {
                this.jsonData = response.data
                console.log(response.data)
            }).catch(error => {
                console.log(error)
            })
        },

        postquery () {
            const path = 'http://127.0.0.1:5000/api/getdata';

            let db = this.jsonData[this.db_index-1].db
            axios.post(path,{
                db: db,
                table:this.tb
            }).then(response => {

                this.dataList = response.data.jsonData.main
                this.tableTh = response.data.jsonData.columns
                this.active_hide = false
                // console.log(response);

            }).catch(error => {
                console.log(error)
            })

        },



    }
}
</script>
