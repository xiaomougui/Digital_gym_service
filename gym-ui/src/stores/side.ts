import { defineStore } from 'pinia'

interface SideState {
    isCollapse: boolean
}

export const useSideStore = defineStore('side', {
    state: (): SideState => ({
        isCollapse: true
    }),
    getters: {

    },
    actions: {
        handleSwitch() {
            console.log(this.isCollapse, '658')
            this.isCollapse = !this.isCollapse;
        },
        // handleClose() {
        //     this.isCollapse = false;
        // }
    },
    persist: true // 使用持久化插件
})
