variable "github_token" {
  description = "Token d'accès personnel GitHub"
  type        = string
  sensitive   = true
}

variable "github_owner" {
  description = "Propriétaire du dépôt GitHub (utilisateur ou organisation)"
  type        = string
  default     = "TiPunchLabs"
}

variable "repository_name" {
  description = "Nom du dépôt GitHub"
  type        = string
  default     = "cv-converter"
}

variable "repository_description" {
  description = "Description du dépôt GitHub"
  type        = string
  default     = "cv converter html to pdf and word"
}

variable "repository_visibility" {
  description = "Visibilité du dépôt (public ou private)"
  type        = string
  default     = "public"

  validation {
    condition     = contains(["public", "private"], var.repository_visibility)
    error_message = "La visibilité doit être 'public' ou 'private'."
  }
}
