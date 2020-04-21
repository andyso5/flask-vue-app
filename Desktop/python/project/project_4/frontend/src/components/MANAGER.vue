<template>
    <div>
        <div align="left">
            <h3>查询代码管理</h3>
        
            <table>
                <thead>
                <tr>
                    <!-- <th v-bind:class="{ hide: active_hide}">序号</th> -->
                    <th v-for="th in tableTh" :key="th">
                        {{ th }}
                    </th>
                    <th>选项</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="(col,index) in dataList" :key="index">


                    <td v-for="tr in tableTh" :key="tr">
                        {{col[tr]}}
                        <!-- {{col.th}} -->
                    </td>
                    <button @click="editCode(col)">编辑</button>
                    <button @click="deleteCode(col)">删除</button>

                </tr>
                </tbody>
            </table> 
        </div>
        <!-- <button @click="slice_t()">测试</button> -->
        <!-- <div align="left">
            <h3>查询代码管理</h3>
        </div> -->
    </div>

</template>


<script>
import axios from 'axios'
export default{

    data () {
        return {
            tableTh:[],
            dataList:{},
        }
    },

    created () {
        this.getData()
    },
    methods: {
        getData () {
            const path = 'http://127.0.0.1:5000/api/getdata';
            axios.post(path,{
                db:'rest',
                table:'pycode'

            }).then(response =>{
                this.dataList = response.data.jsonData.main
                this.tableTh = response.data.jsonData.columns.slice(0,-1)

                console.log(this.dataList,this.tableTh)
            }).catch(error =>{
                console.log(error)
            })
        },
        slice_t () {
            let a = [1,2,3,4]
            console.log(a.slice(0,-1))
        },


        editCode (row) {
            this.$router.push({
                path:'/edit-code',
                query:{
                    Content: row,
                    editCols:['name','content']
                }
            })

        },

        deleteCode (col) {
            // console.log(index)
            const path = 'http://127.0.0.1:5000/api/delete_info'
            axios.post(path,{
                name: 'pycode',
                id:col.id
            }).then(response => {
                this.getData()
                alert('是否删除成功：'+(response.data.success))
                console.log(response)
            }).catch(error => (
                console.log(error)
            ))


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
    },
}
</script>