--[[
map-outline.lua — one outline file, two outputs.

Usage in a section file:

  ::: {.map-outline fig="fig-5-1-full"}
  {{< include /outlines/ch05/Some_Map_list.md >}}
  :::

Web (HTML): the nested list is placed in a collapsible <details> box
right under the figure.

Word (docx): the box is replaced by a link, and the outline is turned
into headings (one per list item) in an "Appendix to Chapter N" placed
after the chapter's last section. Each map there is labelled in bold
("Section 5.1, Figure 3"), with a link back to the figure, and its top
claim is Heading 2 — leaving Heading 2–9 (8 levels) for the map.

Chapters and sections are recognised from section titles that start
with their number: "# 5.1 Introduction".

Optional attributes:
  label="..."   custom wording for the collapsible box's summary line
]]

local MAX_WORD_LEVEL = 9
local BASE_LEVEL = 2        -- map's top claim in the Word appendix
local pending = {}          -- appendix blocks waiting for end of chapter
local pending_chapter = nil -- chapter number the pending blocks belong to
local current_chapter = nil
local current_section = nil
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
  local fig = div.attributes["fig"]
  counter = counter + 1
  local desc_id = "desc-" .. (fig or ("map" .. counter))

  if is_docx() then
    -- Appendix entry: bold label (a bookmark) linking back to the figure.
    local label = pandoc.Inlines({})
    if current_section then
      label:insert(pandoc.Str("Section " .. current_section .. ","))
      label:insert(pandoc.Space())
    end
    if fig then
      label:insert(pandoc.Cite({ pandoc.Str("@" .. fig) },
        { pandoc.Citation(fig, "NormalCitation") }))
    else
      label:insert(pandoc.Str("Argument map"))
    end
    table.insert(pending, pandoc.Para({
      pandoc.Strong({ pandoc.Span(label, pandoc.Attr(desc_id)) })
    }))
    for _, blk in ipairs(div.content) do
      if blk.t == "BulletList" or blk.t == "OrderedList" then
        list_to_headings(blk, BASE_LEVEL, pending, fig or desc_id)
      end
    end
    pending_chapter = current_chapter
    -- In the section text: a pointer to the description.
    local where = current_chapter
      and ("appendix to Chapter " .. current_chapter)
      or "appendix"
    return pandoc.Para({
      pandoc.Str("A text description of this map is in the "),
      pandoc.Link(where, "#" .. desc_id),
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

local function appendix()
  local title = pending_chapter
    and ("Appendix to Chapter " .. pending_chapter .. ": Text descriptions of argument maps")
    or "Appendix: Text descriptions of argument maps"
  local out = pandoc.Blocks({
    pandoc.Header(1, title, pandoc.Attr("", {"unnumbered", "unlisted"}))
  })
  out:extend(pending)
  pending = {}
  pending_chapter = nil
  return out
end

-- Walk the whole document. Section titles ("# 5.1 ...") set the current
-- chapter and section; the Word appendix is flushed when the chapter
-- number changes and at the very end.
function Pandoc(doc)
  local result = pandoc.Blocks({})
  for _, blk in ipairs(doc.blocks) do
    if blk.t == "Header" and blk.level == 1 then
      local text = pandoc.utils.stringify(blk.content)
      local ch, sec = text:match("^(%d+)%.(%d+)")
      local new_chapter = ch
      if is_docx() and #pending > 0 and new_chapter ~= pending_chapter then
        result:extend(appendix())
      end
      current_chapter = ch
      current_section = ch and (ch .. "." .. sec) or nil
    end
    if blk.t == "Div" and blk.classes:includes("map-outline") then
      local r = handle_div(blk)
      if r.t then result:insert(r) else result:extend(r) end
    else
      result:insert(blk)
    end
  end
  if is_docx() and #pending > 0 then
    result:extend(appendix())
  end
  doc.blocks = result
  return doc
end

return { { Pandoc = Pandoc } }
