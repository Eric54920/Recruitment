<template>
  <div class="community">
    <div class="container">
      <el-row :gutter="20">
        <el-col :span="4">
          <div class="grid-content">
            <ul class="category">
              <li class="item" @click="panel = 'recom'" :class="{'active': panel == 'recom'}">
                  <i class="fa fa-fire"></i> 为你推荐
              </li>
              <li class="item" @click="panel = 'last'" :class="{'active': panel == 'last'}">
                  <i class="fa fa-globe"></i> 最新内容
              </li>
              <li class="item" v-if="user_id" @click="panel = 'focus'" :class="{'active': panel == 'focus'}">
                  <i class="fa fa-heart"></i> 我关注的
              </li>
              <span class="split">技术频道</span>
              <el-collapse accordion>
                <el-collapse-item v-for="(item, i) in articleCategory" :key="i" :title="item.title">
                    <li class="item" v-for="(sub_item, j) in item.children" :key="j" @click="panel = sub_item"  :class="{'active': panel == sub_item}">
                        {{ sub_item }}
                    </li>
                </el-collapse-item>
            </el-collapse>
            </ul>
          </div>
        </el-col>
        <el-col :span="15">
          <div class="grid-content">
            <article class="article" v-for="(item, i) in articles.results" :key="i">
                <header class="title"><a :href="`/article/${item.id}`" target="_blank">{{ item.title }}</a></header>
                <p class="content" v-html="item.html_code"></p>
                <div class="info">
                    <span><i class="fa fa-thumbs-up star" @click="like(item.id)"></i> {{ item.like }}</span>
                    <span><i class="fa fa-commenting"></i> {{ item.comment }}</span>
                    <span><a :href="`/user/${item.user}`"><i class="fa fa-user-secret"></i> {{ item.userinfo.nic_name }}</a></span>
                    <span><i class="fa fa-clock-o"></i> {{ item.pub_date | endOf }}</span>
                </div>
            </article>
            <el-pagination
                background
                @current-change="handleCurrentChange"
                layout="prev, pager, next"
                :total="articles.count">
            </el-pagination>
          </div>
        </el-col>
        <el-col :span="5">
          <div class="grid-content">
                <el-carousel :interval="5000" arrow="always">
                    <el-carousel-item v-for="item in 3" :key="item">
                    <h3>{{ item }}</h3>
                    </el-carousel-item>
                </el-carousel>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
import moment from "moment";
export default {
    data () {
        return {
            user_id: '',
            panel: 'recom',
            articleCategory: this.settings.articleCategory,
            articles: [],
            filters: { // 分页条件
                page: 1
            },
            currentDate: new Date()
        }
    },
    filters: {
        dateStr: function(value, format="YYYY-MM-DD HH:mm:ss") {
        return moment(value).format(format);
        },
        endOf: function(value, format = "YYYYMMDD") {
        return moment(value, "YYYYMMDD").fromNow();
        }
    },
    watch: {
        "filters.page" () {
            this.getArticles();
        },
        "panel" () {
            this.getArticles();
        }
    },
    created () {
        this.user_id = sessionStorage.user_id;
        this.getArticles();
    },
    methods: {
        //获取文章
        async getArticles () {
            if (this.panel == 'recom') {
                let response = await this.axios.get(`${this.settings.Host}/article/`, {
                    params: this.filters
                });
                this.articles = response.data;
            } else if (this.panel == 'last') {
                let response = await this.axios.get(`${this.settings.Host}/article/`, {
                    params: this.filters
                });
                this.articles = response.data;
            } else if (this.panel == 'focus') {
                let response = await this.axios.get(`${this.settings.Host}/article/focus/${this.user_id}/`, {
                    params: this.filters
                });
                this.articles = response.data;
            } else {
                let response = await this.axios.get(`${this.settings.Host}/article/?tag=${this.panel}`, {
                    params: this.filters
                });
                this.articles = response.data;
            }
        },
        // 处理分页
        handleCurrentChange (page) {
            this.filters.page = page;
        },
        like (id) {
            if (this.user_id) {
                this.axios.post(`${this.settings.Host}/article/like/`, {
                    user: this.user_id,
                    article_id: id
                }).then(res => {
                    if (res.status == 200) {
                        this.getArticles();
                    } else {
                        this.$message("该用户不存在");
                    }
                }).catch(err => {
                    this.$message('网络异常');
                })
            } else {
                this.$message('登录之后才能评论哦');
            }
        }
    }
};
</script>

<style lang="less" rel="stylesheet/less">
.community {
    padding-top: 20px;
    .container {
        .el-row {
            margin-bottom: 20px;
            &:last-child {
            margin-bottom: 0;
            }
            .el-col {
                border-radius: 4px;
                .grid-content {
                    border-radius: 4px;
                    min-height: 36px;
                    .category {
                        padding: 10px 0;
                        .item {
                            height: 35px;
                            line-height: 35px;
                            padding: 0 10px;
                            font-size: 14px;
                            font-weight: 500;
                            color: #666;
                            border-radius: 5px;
                            text-transform: capitalize;
                            text-overflow: ellipsis;
                            overflow: hidden;
                            white-space: nowrap;
                            cursor: pointer;
                            transition: all .3s;
                            .fa {
                                margin-right: 10px;
                            }
                        }
                        .active {
                            background-color: #2fa4fe;
                            color: #fff;
                        }
                        .split {
                            position: relative;
                            display: inline-block;
                            font-size: 14px;
                            color: #333;
                            padding: 5px 10px;
                            margin: 5px 0;
                            font-weight: 500;
                            &::after {
                                position: absolute;
                                content: '';
                                width: 101px;
                                height: 1px;
                                background-color: #c3c3c3;
                                right: -96px;
                                top: 50%;
                            }
                        }
                        .el-collapse {
                            border: none;
                            .el-collapse-item {
                                & > div {
                                    padding: 0 10px;
                                    .el-collapse-item__header {
                                        font-size: 14px;
                                    }
                                }
                            }
                        }
                    }
                    .article {
                        margin-bottom: 40px;
                        .title {
                            font-size: 18px;
                            font-weight: 500;
                            line-height: 30px;
                            text-overflow: ellipsis;
                            white-space: nowrap;
                            overflow: hidden;
                            a {
                                color: #333;
                            }
                        }
                        .content  {
                            display: -webkit-box;
                            -webkit-box-orient: vertical;
                            -webkit-line-clamp: 2;
                            overflow: hidden;
                            text-overflow: ellipsis;
                            max-height: 42px;
                            * {
                                font-size: 14px;
                                color: #666;
                            }
                            img {
                                display: none;
                            }
                        }
                        .info {
                            span {
                                a {
                                    color: #666;
                                }
                                margin-right: 20px;
                                color: #666;
                                font-size: 13px;
                                .fa {
                                    width: 20px;
                                    height: 20px;
                                    line-height: 20px;
                                    text-align: center;
                                    color: #2fa4fe;
                                    cursor: pointer;
                                }
                                .star {
                                    &:hover {
                                        background-color: #2ea4fe;
                                        border-radius: 50%;
                                        color: #fff;
                                    }
                                }
                            }
                        }
                    }
                    .el-pagination {
                        text-align: center;
                    }
                    .el-carousel__item h3 {
                        color: #475669;
                        font-size: 18px;
                        opacity: 0.75;
                        line-height: 300px;
                        margin: 0;
                    }
                    
                    .el-carousel__item:nth-child(2n) {
                        background-color: #99a9bf;
                    }
                    
                    .el-carousel__item:nth-child(2n+1) {
                        background-color: #d3dce6;
                    }
                }
            }
        }
    }
}
</style>