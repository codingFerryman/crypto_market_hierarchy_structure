<template>
  <div class="w-full flex justify-center">
    <ul
      role="list"
      class="w-2/3"
    >
      <li
        v-for="result in results"
        :key="result.repo"
        class="
          relative
          pl-4
          pr-6
          py-5
          sm:py-6 sm:pl-6
          lg:pl-8
          xl:pl-6
        "
      >
        <div class="flex items-center justify-between space-x-4">
          <!-- Repo name and link -->
          <div class="min-w-0 space-y-3">
            <div class="flex items-center space-x-3">
              <span class="block">
                <p class="text-sm font-medium text-gray-500">
                  <a :href="result.tf_image_model_url">
                    <span class="absolute" aria-hidden="true" />
                    {{ result.tf_image_model_url }}
                  </a>
                </p>
              </span>
            </div>
            <a :href="result.tf_image_model_url">
              <span
                class="
                  text-lg text-indigo-600
                  font-medium
                  truncate
                  hover:underline
                "
                aria-hidden="false"
              >
                {{ result.repo }}
              </span>
            </a>
          </div>
          <!-- Repo meta info -->
          <div
            class="hidden sm:flex flex-col flex-shrink-0 items-end space-y-3"
          >
            <p class="flex text-gray-500 text-sm space-x-2">
              <span>{{ result.err }}</span>
              <span aria-hidden="true">&middot;</span>
            </p>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
const results = [
  {
    tf_image_model_url:
      "https://tfhub.dev/google/imagenet/mobilenet_v1_100_224/feature_vector/4",
    output_key: null,
    required_image_size: { height: 224, width: 224 },
    classifier: "Linear(learning_rate=0.01 num_epochs=2000)",
    err: 0.1303921568627451,
    classify_job_hash:
      "b2640651e91a9f624916d712634a614d96f0a4364e17cc7c4c27432df60daf7b",
    test_reader_name: null,
    start: null,
    stop: null,
    repo: "imagenet/mobilenet_v1_100_224",
  },
];

export default {
  setup() {
    return {
      results,
    };
  },
};
</script>
