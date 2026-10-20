{# Extend the pinned renderer rather than duplicating its full preamble. #}
// A small running heading identifies a section carried over from a prior page.
#set page(header: context {
    let current = here().page()
    let sections = query(heading.where(level: 2))
    let endings = query(<cv-section-end>)
    let preceding = sections.filter(it => it.location().page() < current)
    if preceding.len() > 0 {
      let index = preceding.len() - 1
      if endings.at(index).location().page() >= current {
        text(size: 9pt, fill: {{ design.colors.footer.as_rgb() }})[
          #preceding.last().body (continued)
        ]
      }
    }
})

{% include "typst/Preamble.j2.typ" %}
