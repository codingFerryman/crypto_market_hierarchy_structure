<template>
 <div class="flex justify-center">
    <div class="w-1/3 text-center">
      <h1 class="w-full leading-6 text-2xl text-gray-900">
        S.E.A.L Search
      </h1>
      <div class="mt-5 lg:flex lg:items-center w-full mb-5">
        <div class="w-full">
            <label for="search" class="sr-only">Search</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <SearchIcon class="h-5 w-5 text-gray-400" aria-hidden="true" />
              </div>
              <input id="search" name="search" class="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" placeholder="Search" type="search" />
            </div>
          </div>
      </div>
      <div class="w-full">
        <NuxtLink to="result"> 
        <button type="submit" class="mt-3 w-full inline-flex items-center justify-center px-4 py-2 border border-transparent font-medium rounded-md text-gray-600 bg-slate-100 hover:bg-slate-200 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
            Search
        </button></NuxtLink>
        <button type="submit" class="mt-3 w-full inline-flex items-center justify-center px-4 py-2 font-medium rounded-md text-gray-600 bg-slate-100 hover:bg-slate-200 focus:outline-none sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm">
            Advanced Usage
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { SearchIcon } from '@heroicons/vue/solid'

export default {
  components: {
    SearchIcon,
  },
}
</script>