<script lang="ts" setup>
import "./assets/css/tailwind.css";
</script>

<template>
  <NuxtLayout id="page-container">
    <NuxtPage id="content-wrap"/>
    <Footer id="footer"/>
  </NuxtLayout>
</template>

<style>
#page-container {
  position: relative;
  min-height: 100vh;
}

#content-wrap {
  padding-bottom: 2.5rem;    /* Footer height */
}

#footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  height: 2.5rem;            /* Footer height */
}
</style>