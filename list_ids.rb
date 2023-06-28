#!/usr/bin/env ruby
# frozen_string_literal: true

require 'csv'
require 'optimist'
require 'rexml/document'

# An instance of this class is an XML rule.
class Rule
  include REXML

  COMMENT_PATTERN = /foo/.freeze

  HEADERS = %w[id comment default].freeze

  extend Forwardable
  def_delegators :@element, :attributes, :children

  def initialize(element)
    @element = element
    attributes.each do |attribute, value|
      instance_variable_set("@#{attribute}", value)
      self.class.class_eval { attr_reader attribute.to_sym }
    end
  end

  def comments
    @comments ||= children.select do |child|
      child.is_a?(Comment) and child.string.match?(COMMENT_PATTERN)
    end
  end

  def to_s
    id
  end

  def to_row
    # TODO: figure out how to display comments as a string
    CSV::Row.new(HEADERS, [id, comments, default])
  end
end

# file that defines a single XML rules file
class RulesFile
  include REXML

  attr_reader :xml, :path, :name, :is_premium

  def initialize(path)
    @path = path
    @name = File.basename(@path, '.xml')
    # TODO: read premium from path
    @is_premium = true
    @xml = Document.new(File.read(@path))
  end

  def rules
    @rules ||= xml.root.elements['/rules//category'].filter_map do |el|
      Rule.new(el) if el.is_a?(Element)
    end
  end

  def to_table
    CSV::Table.new(rules.map(&:to_row))
  end
end
