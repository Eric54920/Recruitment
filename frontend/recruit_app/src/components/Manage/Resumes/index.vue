<template>
    <div class="resumes">
        <div class="container">
            <header>推荐简历</header>
            <el-card class="box-card">
                <div class="text item">
                    <table>
                        <tr>
                            <th>简历标题</th>
                            <th>用户</th>
                            <th>修改时间</th>
                        </tr>
                        <tr v-for="(item, i) in resume_list.results" :key="i">
                            <td><el-link :href="`/resume/${item.id}`" target="_blank" :underline="false">{{ item.title }}</el-link></td>
                            <td><el-link :href="`/user/${item.user}`" target="_blank" :underline="false">{{ item.userinfo.nic_name }}</el-link></td>
                            <td><h1>{{ item.update_date | dateStr }}</h1></td>
                        </tr>
                    </table>
                </div>
            </el-card>
        </div>
    </div>
</template>

<script>
import moment from "moment";
export default {
    data () {
        return {
            resume_list: {}
        }
    },
    filters: {
        dateStr: function(value, format="YYYY-MM-DD HH:mm:ss") {
            return moment(value).format(format);
        },
    },
    created () {
        this.getResumes();
    },
    methods: {
        async getResumes () {
            let response = await this.axios.get(`${this.settings.Host}/resume/`)
            this.resume_list = response.data;
        }
    }
};
</script>

<style lang="less" rel="stylesheet/less">
.resumes {
    min-height: 500px;
    padding-top: 20px;
    .container {
        header {
            width: 840px;
            margin: 0 auto;
            padding: 20px 0;
            font-size: 32px;
            color: #333;
        }
        .box-card {
            width: 840px;
            margin: 0 auto 20px;
            .item {
                table {
                    width: 100%;
                    tr {
                        height: 50px;
                        line-height: 50px;
                        text-align: left;
                        border-bottom: 1px solid #e6e6e6;
                        td {
                            h1 {
                                color: #606266;
                                font-size: 14px;
                            }
                        }
                    }
                }
            }
        }
    }
}
</style>