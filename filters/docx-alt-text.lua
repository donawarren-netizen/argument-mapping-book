--[[
docx-alt-text.lua — copy each image's fig-alt into Word's alt text.
Quarto puts fig-alt into the web version but not into Word, where the
alt text otherwise ends up as the image's file path.
]]
function Image(img)
  if not quarto.doc.is_format("docx") then return nil end
  local alt = img.attributes["fig-alt"]
  if alt and alt ~= "" then
    img.caption = pandoc.Inlines({ pandoc.Str(alt) })
    return img
  end
end
