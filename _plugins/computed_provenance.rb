# frozen_string_literal: true

require "json"

module Jekyll
  # Expose the checked computed-artifact manifest to Liquid without duplicating
  # version metadata in a second source file.
  class ComputedProvenanceGenerator < Generator
    safe true
    priority :highest

    def generate(site)
      path = site.in_source_dir("assets", "img", "research", "computed", "provenance.json")
      manifest = JSON.parse(File.read(path))
      unless manifest["schema_version"] == 1 && manifest["packages"].is_a?(Hash) && !manifest["packages"].empty?
        raise Jekyll::Errors::FatalException, "Unsupported computed-artifact provenance manifest"
      end

      site.data["computed_provenance"] = manifest
    rescue Errno::ENOENT, JSON::ParserError => e
      raise Jekyll::Errors::FatalException, "Cannot load computed-artifact provenance: #{e.message}"
    end
  end
end
