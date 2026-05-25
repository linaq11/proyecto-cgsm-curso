--[[
Filtro Lua para Quarto/Pandoc que convierte cada tabla pipe a un entorno
LaTeX `tblr` (de tabularray) con cuadrícula completa --hlines+vlines--
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

  -- Construir column-spec con anchos relativos SIEMPRE proporcionales a \linewidth.
  -- Si Pandoc no aporta widths (todas las celdas con cs[2]==0), distribuimos uniforme.
  local col_specs = {}
  local widths = {}
  local total_w = 0
  for _, cs in ipairs(tbl.colspecs) do
    table.insert(col_specs, ALIGN_TO_TBLR[cs[1]] or 'l')
    local w = (cs[2] and cs[2] > 0) and cs[2] or 0
    table.insert(widths, w)
    total_w = total_w + w
  end
  local n = #col_specs

  -- Si no hay widths del Markdown, repartir uniformemente para evitar overflow.
  if total_w == 0 then
    for i = 1, n do widths[i] = 1 / n end
    total_w = 1
  end

  -- Construir colspec usando X[weight, align] de tabularray.
  -- X distribuye automáticamente el ancho disponible (= \linewidth en tblr)
  -- proporcional a los weights. Multiplicamos por 100 y redondeamos para
  -- obtener weights enteros estables.
  local colspec_parts = {}
  for i = 1, n do
    local weight = math.max(1, math.floor((widths[i] / total_w) * 100 + 0.5))
    table.insert(colspec_parts,
      string.format('X[%d,%s]', weight, col_specs[i]))
  end
  local colsig = 'colspec={' .. table.concat(colspec_parts, '') .. '}'

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
    label = tbl.attr.identifier
  end

  -- Armar tblr (sin page-break) dentro de un float table con caption + label.
  -- Esto produce cuadrícula completa sin "Tabla X: (Continued)" entre filas.
  local lines = {}
  table.insert(lines, '\\begin{table}[H]')
  table.insert(lines, '\\centering')
  if cap_latex ~= '' then
    if label ~= '' then
      table.insert(lines, '\\caption{' .. cap_latex .. '}\\label{' .. label .. '}')
    else
      table.insert(lines, '\\caption{' .. cap_latex .. '}')
    end
  elseif label ~= '' then
    table.insert(lines, '\\label{' .. label .. '}')
  end

  table.insert(lines, '\\begin{tblr}{')
  table.insert(lines, '  ' .. colsig .. ',')
  table.insert(lines, '  hlines={black!50, 0.3pt},')
  table.insert(lines, '  vlines={black!50, 0.3pt},')
  table.insert(lines, '  row{1}={font=\\bfseries\\scriptsize},')
  table.insert(lines, '  rowsep=1.5pt,')
  table.insert(lines, '  stretch=0')
  table.insert(lines, '}')

  for _, h in ipairs(header_rows) do
    table.insert(lines, h .. ' \\\\')
  end
  for _, r in ipairs(body_rows) do
    table.insert(lines, r .. ' \\\\')
  end

  table.insert(lines, '\\end{tblr}')
  table.insert(lines, '\\end{table}')

  return pandoc.RawBlock('latex', table.concat(lines, '\n'))
end
