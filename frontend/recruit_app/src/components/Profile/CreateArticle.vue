<template>
  <div class="create-article">
    <div class="container">
        <header>创建文章</header>
        <div class="editor">
            <div id="main">
                <div class="article-desc">
                    <el-form :label-position="labelPosition" label-width="80px" :model="articleInfo">
                        <el-form-item label="标题">
                            <el-input v-model="articleInfo.title"></el-input>
                        </el-form-item>
                        <el-form-item label="标签">
                            <p ref="tag">
                                <el-button size="mini" @click="tagsPanel=true"><i class="fa fa-plus-circle"></i> 标签</el-button>
                                <el-tag v-for="(item, i) in articleInfo.tags" :key="i" size="medium" closable type="info" :disable-transitions="false" @close="handleClose(item)" style="margin-right: 10px;cursor:pointer;">{{ item }}</el-tag>    
                            </p>
                            <el-tabs type="border-card" v-if="tagsPanel">
                                <el-tab-pane v-for="(item, i) in articleTags" :key="i" :label="item.title">
                                    <el-tag v-for="(subitem, i) in item.children" :key="i" size="medium" type="info" @click="addTag(subitem)" style="margin:10px;cursor:pointer;">{{ subitem }}</el-tag>
                                </el-tab-pane>
                            </el-tabs>
                        </el-form-item>
                    </el-form>
                </div>
                <mavon-editor 
                    :subfield=false
                    :ishljs = "true"
                    boxShadowStyle="0 2px 12px 0 rgba(255, 255, 255, 0)"
                    v-model="articleValue" 
                    ref=md @imgAdd="imgAdd"
                    :toolbars="toolbars"
                    @save="saveArticle"
                    placeholder="点击全屏实时预览"
                    style="min-height:500px"
                    >
                </mavon-editor>
                <div class="operate">
                    <a href="javascript:;" @click="saveArticle">发表</a>
                </div>
            </div>
        </div>
    </div>
  </div>
</template>

<script>
export default {
    data () {
        return {
            user_id: '',
            labelPosition: 'left',
            articleValue: '',
            articleInfo: { // 文章信息
                title: '',
                tags: []
            },
            toolbars: this.settings.toolbars,
            tagsPanel: false,
            articleTags: {}
        }
    },
    created () {
        this.user_id = sessionStorage.user_id;
        this.articleTags = this.settings.articleCategory;
    },
    methods: {
        // 绑定@imgAdd event
        imgAdd(pos, $file){
            // 第一步.将图片上传到服务器.
            var formdata = new FormData();
            formdata.append('image', $file);
            axios({
                url: 'http://api.offend.com:8000/avatar/',
                method: 'post',
                data: formdata,
                headers: { 'Content-Type': 'multipart/form-data' },
            }).then((url) => {
                // 第二步.将返回的url替换到文本原位置![...](./0) -> ![...](url)
                /**
             * $vm 指为mavonEditor实例，可以通过如下两种方式获取
             * 1. 通过引入对象获取: `import {mavonEditor} from ...` 等方式引入后，`$vm`为`mavonEditor`
             * 2. 通过$refs获取: html声明ref : `<mavon-editor ref=md ></mavon-editor>，`$vm`为 `this.$refs.md`
             */
                $vm.$img2Url(pos, url);
            })
        },
        // 保文章
        saveArticle() {
            this.axios.post(`${this.settings.Host}/article/`, {
                user: this.user_id,
                title: this.articleInfo.title,
                tag: this.articleInfo.tags.join('|'),
                html_code: this.$refs.md.d_render,
                md_code: this.$refs.md.d_value
            }).then(response => {
                this.articleValue = "";
                this.articleInfo = {};
                this.$notify({
                    title: '成功',
                    message: '文章发表成功',
                    type: 'success'
                });
            }).catch(error => {
                this.$notify({
                    title: '失败',
                    message: '请检查是否有空白选项',
                    type: 'error'
                });
            })
        },
        // 添加标签
        addTag (str) {
            if (this.articleInfo.tags.indexOf(str) == '-1') {
                if (this.articleInfo.tags.length < 5) {
                    this.articleInfo.tags.push(str);
                }
            }
        },
        // 移除标签
        handleClose(tag) {
            this.articleInfo.tags.splice(this.articleInfo.tags.indexOf(tag), 1);
        },
    }
}
</script>

<style lang="less" rel="stylesheet/less">
.create-article {
    background-color: #f6f6f6;
    .container {
        header {
            width: 840px;
            margin: 0 auto;
            padding: 20px 0;
            font-size: 32px;
            color: #333;
        }
        .editor {
            margin: 0 auto 20px;
            width: 840px;
            background-color: #fff;
            border-radius: 10px;
            margin-bottom: 20px;
            #main {
            .article-desc {
                padding: 25px 25px 0 25px;
            }
            .operate {
                padding: 10px;
                display: flex;
                flex-wrap: nowrap;
                flex-direction: row-reverse;
                a {
                    display: inline-block;
                    color: #ffffff;
                    padding: 5px 10px;
                    background-color: #2fa4fe;
                    border-radius: 5px;
                }
            }
            }
        }
    }
}
</style>