resource "kubernetes_manifest" "app" {
  for_each = fileset("${path.module}/../kubernetes", "*.yaml")
  manifest = yamldecode(file("${path.module}/../kubernetes/${each.key}"))
}
