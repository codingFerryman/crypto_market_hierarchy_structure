<template>
  <main id="page-container" class="px-4 py-10 text-center text-gray-700 dark:text-gray-200">
    <router-view id="page-wrap"/>
    <Footer id="footer"/>
  </main>
</template>

<style scoped>
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
