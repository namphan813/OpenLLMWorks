export function gpuSlug(gpuModel) {
  return gpuModel
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}