--[[
Filtro Lua para Quarto/Pandoc que convierte cada tabla pipe a un entorno
LaTeX `longtblr` (de tabularray) con cuadrícula completa --hlines+vlines--
en lugar del estilo booktabs que solo dibuja líneas horizontales.

Requiere en el preámbulo LaTeX:
    \usepackage{tabularray}
    \UseTblrLibrary{booktabs}
    \UseTblrLibrary{varwidth}

Activación en el YAML del .qmd:
    filters:
      - _filters/grid_tables.lua

Solo actúa en salida latex/pdf; en HTML y DOCX la tabla pasa intacta.
]]--

local ALIGN_TO_TBLR = {
  AlignLeft   = 'l',
  AlignRight  = 'r',
  AlignCenter = 'c',
  AlignDefault = 'l',
}

local function cell_to_latex(cell)
  -- Convierte el contenido de una celda (lista de Blocks) a LaTeX inline
  if cell.contents == nil or #cell.contents == 0 then return '' end
  local doc = pandoc.Pandoc(cell.contents)
  local latex = pandoc.write(doc, 'latex')
  -- Quitar saltos de línea y trim
  latex = latex:gsub('\n+$', ''):gsub('^%s+', ''):gsub('%s+$', '')
  return latex
end

local function row_to_latex(row)
  local cells = {}
  for _, cell in ipairs(row.cells) do
    table.insert(cells, cell_to_latex(cell))
  end
  return table.concat(cells, ' & ')
end

function Table(tbl)
  if not (FORMAT:match('latex') or FORMAT:match('pdf')) then
    return tbl
  end

  -- Construir column-spec con anchos relativos si están definidos
  local col_specs = {}
  local widths = {}
  for _, cs in ipairs(tbl.colspecs) do
    table.insert(col_specs, ALIGN_TO_TBLR[cs[1]] or 'l')
    if cs[2] and cs[2] > 0 then
      table.insert(widths, string.format('%.2f', cs[2]))
    end
  end
  local n = #col_specs
  -- tabularray colspec acepta cadena tipo "lcr" sin comas; usar forma corta
  local colsig = 'colspec={' .. table.concat(col_specs, '') .. '}'

  -- Construir filas del cuerpo
  local header_rows = {}
  if tbl.head and tbl.head.rows then
    for _, row in ipairs(tbl.head.rows) do
      table.insert(header_rows, row_to_latex(row))
    end
  end

  local body_rows = {}
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      table.insert(body_rows, row_to_latex(row))
    end
  end

  -- Caption y label
  local cap_latex = ''
  local label = ''
  if tbl.caption and tbl.caption.long and #tbl.caption.long > 0 then
    cap_latex = pandoc.write(pandoc.Pandoc(tbl.caption.long), 'latex')
    cap_latex = cap_latex:gsub('\n+$', '')
  end
  if tbl.attr and tbl.attr.identifier and tbl.attr.identifier ~= '' then
    label = '\\label{' .. tbl.attr.identifier .. '}'
  end

  -- Armar el entorno longtblr con cuadrícula completa
  local lines = {}
  table.insert(lines, '\\begin{longtblr}[')
  if cap_latex ~= '' then
    table.insert(lines, '  caption={' .. cap_latex .. '},')
  end
  if label ~= '' then
    table.insert(lines, '  label={' .. (tbl.attr.identifier or '') .. '},')
  end
  table.insert(lines, ']{')
  table.insert(lines, '  ' .. colsig .. ',')
  table.insert(lines, '  hlines, vlines,')
  table.insert(lines, '  rowhead = ' .. tostring(#header_rows) .. ',')
  table.insert(lines, '  row{1}={font=\\bfseries},')
  table.insert(lines, '  rowsep=2pt')
  table.insert(lines, '}')

  for _, h in ipairs(header_rows) do
    table.insert(lines, h .. ' \\\\')
  end
  for _, r in ipairs(body_rows) do
    table.insert(lines, r .. ' \\\\')
  end

  table.insert(lines, '\\end{longtblr}')

  return pandoc.RawBlock('latex', table.concat(lines, '\n'))
end
