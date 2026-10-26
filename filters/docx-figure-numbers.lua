--[[
docx-figure-numbers.lua — restart figure numbering at each section in Word.

On the web every section is its own page, so Quarto numbers figures
1, 2, 3 on each page. In Word the whole book is one document, and Quarto
numbers figures straight through (Figure 134 …). This filter renumbers
the Word version so each section starts again at Figure 1, matching the web.

Sections are recognised from titles starting with their number ("# 5.1 …").
]]

if not quarto.doc.is_format("docx") then return {} end

local numbers = {}      -- figure id -> number within its section
local section_count = 0

local function caption_inlines(float)
  local cap = float.caption_long
  if cap == nil then return pandoc.Inlines({}) end
  if cap.t == "Plain" or cap.t == "Para" then return cap.content end
  return pandoc.utils.blocks_to_inlines(pandoc.Blocks(cap))
end

return {
  {
    -- Pass 1 (document order): number figures within each section and
    -- replace Quarto's figure with a plain captioned figure.
    traverse = "topdown",
    Header = function(h)
      if h.level == 1 then section_count = 0 end
      return nil
    end,
    FloatRefTarget = function(float)
      if float.type ~= "Figure" or not float.identifier:match("^fig%-") then
        return nil
      end
      section_count = section_count + 1
      local n = section_count
      numbers[float.identifier] = n
      local cap = pandoc.Inlines({ pandoc.Str("Figure " .. n .. ":"), pandoc.Space() })
      cap:extend(caption_inlines(float))
      local content = float.content
      if content.t then content = pandoc.Blocks({ content }) end
      return pandoc.Figure(content, { long = { pandoc.Plain(cap) } },
        pandoc.Attr(float.identifier))
    end,
  },
  {
    -- Pass 2: fix the text of every link to a figure ("Figure 7" -> "Figure 1").
    Link = function(link)
      local id = link.target:match("^#(fig%-.+)$")
      if id and numbers[id] then
        local text = pandoc.utils.stringify(link.content)
        local new = text:gsub("%d+$", tostring(numbers[id]))
        link.content = pandoc.Inlines({ pandoc.Str(new) })
        return link
      end
    end,
  },
}
