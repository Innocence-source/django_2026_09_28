
const API = {

    addTask(taskname) {
        // 要求使用 表单 提交数据
        return axios.post('/tasks/task-add', {name: taskname}, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
    },

    findTaskList() {
        return axios.get("/tasks/task-list") ;
    },

    deleteTaskById(taskId) {
        return axios.delete(`/tasks/task-delete/${taskId}`)
    },

    doneTask(taskId) {
        return axios.put(`/tasks/task-state/${taskId}`) ;
    },

    modifyTaskName({id, name}) {
        return axios.post(`/tasks/task-modify/${id}`, {name: name}, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
    },

    // ==================== 故事类型管理接口 ====================

    // 查询所有故事类型
    findStoryTypeList() {
        return axios.get("/story-type/query");
    },

    // 添加故事类型
    addStoryType(typeName) {
        return axios.post('/story-type/add', {name: typeName}, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        });
    },

    // 修改故事类型
    updateStoryType({id, name, state}) {
        return axios.post(`/story-type/update/${id}`, {name: name, state: state}, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        });
    },

    // 删除故事类型
    deleteStoryType(typeId) {
        return axios.delete(`/story-type/delete/${typeId}`);
    },

    // 切换故事类型启用状态
    toggleStoryTypeState(typeId) {
        return axios.put(`/story-type/state/${typeId}`);
    },

    findStoryTypeList() {
        return axios.get("/story-type/list") ;
    },

    generatorStory({title,type, font_count,keywords, bg_settings,  role_desc, story_detail}) {

        // return axios.post('/story-generator', {title,type, font_count,keywords: keywords.join(","), bg_settings,  role_desc, story_detail}, {
        //     headers: {
        //         "Content-Type": "application/x-www-form-urlencoded"
        //     }
        // })
        const obj = {title,type, font_count, keywords: keywords.join(", "), bg_settings,  role_desc, story_detail}; 
        // 组装 传入的参数 
        const params = new URLSearchParams();
        for(let key in obj) {
            params.append(key, obj[key])
        }

        return fetch("/story-generator", {
            method: "post", 
            body: params, 
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            }
        })
    }

}