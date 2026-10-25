--[[
map-outline.lua — one outline file, two outputs.

Usage in a chapter:

  ::: {.map-outline fig="fig-amuseful"}
  {{< include outlines/ch05/Some_Map_list.md >}}
  :::

Web (HTML): the nested list is placed in a collapsible <details> box
right under the figure.

Word (docx): the box is replaced by a link, and the outline is turned
into headings (one per list item) in a "Text descriptions" section at
the end of the chapter, with a link back to the figure.

Optional attributes:
  label="..."   custom wording for the collapsible box's summary line
  base-level=3  heading level for the map's top claim in Word (default 3)
]]

local MAX_WORD_LEVEL = 9
local pending = {}          -- appendix blocks waiting for end of chapter
local counter = 0

local function is_docx()
  return quarto.doc.is_format("docx")
end

-- Turn a nested bullet list into headings, starting at `level`.
local function list_to_headings(list, level, out, map_id)
  for _, item in ipairs(list.content) do
    local inlines = pandoc.Inlines({})
    local sublists = {}
    for _, blk in ipairs(item) do
      if blk.t == "BulletList" or blk.t == "OrderedList" then
        table.insert(sublists, blk)
      elseif blk.t == "Plain" or blk.t == "Para" then
        if #inlines > 0 then inlines:insert(pandoc.Space()) end
        inlines:extend(blk.content)
      end
    end
    if level > MAX_WORD_LEVEL then
      io.stderr:write(string.format(
        "WARNING [map-outline]: %s needs heading level %d; Word stops at %d.\n",
        map_id, level, MAX_WORD_LEVEL))
    end
    local h = pandoc.Header(math.min(level, MAX_WORD_LEVEL), inlines,
      pandoc.Attr("", {"unnumbered", "unlisted"}))
    table.insert(out, h)
    for _, sl in ipairs(sublists) do
      list_to_headings(sl, level + 1, out, map_id)
    end
  end
end

local function handle_div(div)
  if not div.classes:includes("map-outline") then return nil end

  local fig = div.attributes["fig"]
  counter = counter + 1
  local desc_id = "desc-" .. (fig or ("map" .. counter))

  if is_docx() then
    local base = tonumber(div.attributes["base-level"] or "3")
    -- Appendix entry: bookmark + link back to the figure, then headings.
    local intro = pandoc.Inlines({ pandoc.Str("Text description of ") })
    if fig then
      intro:insert(pandoc.Cite({ pandoc.Str("@" .. fig) },
        { pandoc.Citation(fig, "NormalCitation") }))
    else
      intro:insert(pandoc.Str("argument map"))
    end
    table.insert(pending, pandoc.Para({
      pandoc.Strong({ pandoc.Span(intro, pandoc.Attr(desc_id)) })
    }))
    for _, blk in ipairs(div.content) do
      if blk.t == "BulletList" or blk.t == "OrderedList" then
        list_to_headings(blk, base, pending, fig or desc_id)
      end
    end
    -- In the chapter body: a pointer to the description.
    return pandoc.Para({
      pandoc.Str("A text description of this map is at the "),
      pandoc.Link("end of this section", "#" .. desc_id),
      pandoc.Str(".")
    })
  end

  if quarto.doc.is_format("html") then
    local label = div.attributes["label"] or "Text description of the map above"
    local blocks = pandoc.Blocks({
      pandoc.RawBlock("html",
        '<details class="map-outline" id="' .. desc_id .. '">\n<summary>' ..
        label .. '</summary>')
    })
    blocks:extend(div.content)
    blocks:insert(pandoc.RawBlock("html", "</details>"))
    return blocks
  end

  return div.content
end

local function appendix_section()
  local out = pandoc.Blocks({
    pandoc.Header(2, "Text descriptions of this section’s argument maps",
      pandoc.Attr("", {"unnumbered", "unlisted"}))
  })
  out:extend(pending)
  pending = {}
  return out
end

-- Walk the whole document; flush the Word appendix before each new
-- chapter (level-1 heading) and at the very end.
function Pandoc(doc)
  local result = pandoc.Blocks({})
  local function walk_blocks(blocks)
    for _, blk in ipairs(blocks) do
      if is_docx() and blk.t == "Header" and blk.level == 1 and #pending > 0 then
        result:extend(appendix_section())
      end
      if blk.t == "Div" and blk.classes:includes("map-outline") then
        local r = handle_div(blk)
        if r then
          if r.t then result:insert(r) else result:extend(r) end
        end
      else
        result:insert(blk)
      end
    end
  end
  walk_blocks(doc.blocks)
  if is_docx() and #pending > 0 then
    result:extend(appendix_section())
  end
  doc.blocks = result
  return doc
end

return { { Pandoc = Pandoc } }
