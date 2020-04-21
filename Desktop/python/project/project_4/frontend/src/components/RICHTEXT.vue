<template>
<div>
    <vue-editor v-model="content" :editor-toolbar="customToolbar"/>
    <button @click="getMsg()">测试</button>
</div>
</template>


<script>
import { VueEditor } from "vue2-editor";
export default {
    components: { VueEditor },
    data: () => ({
        content:"Some initial content",
        customToolbar:[[""],],
    }),

    methods: {
        getMsg() {
            console.log(this.content)
            this.normalize(this.content)
        },

        normalize (content) {
            let res = content.replace('<p>','')
            res = res.replace('<\/p>','\n')
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


    },

    created () {
        this.htmlize('asdf\naefwe')
    },




}
</script>