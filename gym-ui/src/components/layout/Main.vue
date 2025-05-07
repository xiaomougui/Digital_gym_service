<template>
    <div class="mainview">
        <Side></Side>
        <div class="rightview">
            <HeaderView></HeaderView>
            <router-view></router-view>
        </div>  
    </div>
    
</template>


<script setup lang="ts">
import Side from './Side.vue'
import HeaderView from './HeaderView.vue'
import { RouterView } from 'vue-router';
</script>

<style lang="css" scoped>
.mainview{
    width:100vw;
    height: 100vh;
    display: flex;
}
.rightview{
    flex: 1;
    width: 80%;
}
</style>