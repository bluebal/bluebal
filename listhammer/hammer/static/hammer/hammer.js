
( function( $, ko, store ){
    
    ko.bindingHandlers.blurSubmit={
        init: function( element, valueAccessor, alBindings, viewModel, bingingContext ){
            var form=$( element );
            form.find( 'input[type="text"]').bind( 'blur', function(){
                form.submit();
            });
        }
    };
    ko.bindingHandlers.hammerList={
      init: function( element, valueAccessor, alBindings, viewModel, bingingContext ){
          var hammer=valueAccessor();
         var el=$( element ).sortable({
             handle: '.handle',
             stop: function( e, ui ){
                 var arr=[];
                el.find( '.hammer-item').each( function( i, iel ){
                    arr.push( $( iel ).data( 'pk' ));
                }); 
                hammer.saveItemOrder( arr );
             }
         });
      },
      update: function( element, valueAccessor, alBindings, viewModel, bingingContext ){
          
      }
    };
    /* HAMMER MODEL */
    function Hammer( data, VM ){ 
        var self=this;
        self.VM=VM;
        self.id=ko.observable( data.id || null );
        self.name=ko.observable( data.name || "Unnamed" );
        self.creator=data.creator;//non observable
        self._created=data.created;
        self.created=new Date( data.created ),
        self.cxr=ko.observable( data.cxr || null ); // constructor which passes functionality to plugin(s)
        self.theme=ko.observable( data.theme || 'default' ); // if shared this will be the user overridden theme
        self.shared=data.shared || false; // is this hammer shared with this user?
        self.can_add=data.can_add;
        self.can_remove=data.can_remove;
        self.can_change=data.can_change;
        self.tempTitle=ko.observable();
        self.settingsVisible=ko.observable( false );
        self.settingsHidden=ko.computed( function(){ return !self.settingsVisible(); });
        self.editing=ko.observable( false );
        self.items=ko.observableArray( $.map( data.items || [], function( i ){
           var item=new HammerItem( i ); 
           item.data.subscribe( function(){
                self.saveItem( item );
           });
           return item;
        }));
        self.shares=ko.observableArray( $.map( data.shares || [], function( s ){
            var share=new HammerShare( s );
            share.data.subscribe( function(){
                self.saveShare( share );
            });
            return share;
        }));
        
        /* methods */
        self.addItem=function( data ){
            var item=new HammerItem( data );
            self.items.push( item );
            return item;
        };
        self.addShare=function( data ){
            var share=new HammerShare( data );
            self.shares.push( share );
            return share;
            
        };
        self.destroyShare=function( share ){
            if( confirm( "Do you want to delete this share?")){
                self.removeShare( share );
            }
        }
        self.editItem=function( item ){
            if( !self.can_change ){ return false; }
            item.editing(!item.editing());
        };
        self.saveItemOrder=function( arr ){ // new order of items passed as a list of ids
            if( !self.can_change ) return false;
            return $.ajax({
               type: 'put',
               data: ko.toJSON( arr )
            });
        };
        self.removeItem=function( item ){
            return self.VM.removeItem( item, self )
                .done( function( resp ){
                    if( resp.error ){
                        
                    }
                    else{
                        self.items.remove( item );
                    }
                });
        };
        self.removeShare=function( share ){
          $.ajax({
              url: '/share/',
              data: ko.toJSON({ 'id': share.id(), action: 'delete'})
          }).done( function( resp ){
            self.shares.remove( share );
          });
        };
        self.save=function(){
           return VM.saveHammer( self );
        };
        self.saveItem=function( item ){
            return VM.saveItem( item, self );
        };
        self.saveShare=function( share ){
            return VM.saveShare( share, self );
        };
        self.submitNewItem=function( form ){// form was submitted to add a new item
            if( !self.can_add ) return false;
            
            var input=$( form ).find( 'input[type="text"]'),
                title=input.val(),
                item;
            if( title ){
                item=self.addItem({ title: title });
                input.val('');
                self.saveItem( item ).done( function( resp ){
                    item.data.subscribe( function(){
                       self.saveItem( item ); 
                    });
                    
                });
            }
        };
        self.submitNewShare=function( form ){// form was submitted to add a new share
            if( self.shared ) return false;
            var input=$( form ).find( 'input[ name="sharee" ]'),
                group=input.parent(),
                name=input.val();
            if( name ){
                var exists=self.shares().filter( function( s ){
                    return s.sharee===name;
                }).length > 0;
                if ( !exists ){
                    var share=new HammerShare({ sharee: name });
                    self.saveShare( share ).done( function( resp ){
                        if ( resp.error ){
                            group.addClass( 'has-error');
                        }
                        else{ // successful share creation
                          share.id( resp.id );
                          share.sharee( resp.sharee );
                          self.shares.push( share );
                          share.data.subscribe( function(){
                              self.saveShare( share );
                          });
                          input.val('');
                        }
                    });
                }
                else{
                    console.error( 'Share exists' );
                }
            }

        };
        self.toggleSettings=function(){ console.log( 'toggleSettings' );
          self.settingsVisible( !self.settingsVisible() );  
        };
        self.toJS=function(){
            return {
                id: self.id(),
                name: self.name()
            };
        };
        self.toJSON=function(){
          return ko.toJSON( self.toJS() );
        };
        self.data=ko.computed( function(){ // this is subscribed to in order to detect changes. Overrides will change this
            return self.name();
        });
    }
    
    
    /* HAMMERITEM MODEL */
    function HammerItem( data ){
        var self=this;
        self.id=ko.observable( data.id || null );
        self.title=ko.observable( data.title || "Untitled ");
        self.status=ko.observable( data.status || 'idle');
        self.index=ko.observable( data.index || 0 );
        
        self.editing=ko.observable( false );
        
        self.toggleStatus=function( status1, status2 ){
            var status=self.status();
            self.status( status==status1 ? status2 : status1);
        };
        self._toggleStatus=function(){
            var args=arguments;
            return function(){
              self.toggleStatus.apply( self, args );
            }
        };
        self.toJS=function(){
            var ret={
                id: self.id(),
                title: self.title(),
                status: self.status()
            };
            return ret;
        };
        self.toJSON=function(){
          return ko.toJSON( self.toJS() );  
        };
        self.data=ko.computed( function(){
            return self.title()+''+self.status();
        });
    }
    
    /* HAMMERSHARE MODEL */
    function HammerShare( data ){
        var self=this;
        self.id=ko.observable( data.id || null );
        self.sharee=ko.observable( data.sharee || 'unknown'); // a username
        self.can_add= ko.observable( data.can_add || false );
        self.can_remove= ko.observable( data.can_remove || false );
        self.can_change= ko.observable( data.can_change || false );

        self.data=ko.computed( function(){
           return [ self.can_add(), self.can_change(), self.can_remove() ]; 
        });
    }
    
    /* USER MODEL */
    function User( data ){
        var self=this;
        self.id=data.id;
        self.name=data.name;
        self.date_format=ko.observable( data.date_format );
        self.app_theme=ko.observable( data.app_theme || 'app-theme-default' );
        self.military=ko.observable( data.military );
        
        self.toJS=function(){
          return {
              date_format: self.date_format(),
              military: self.military()
          };
        };
        self.toJSON=function(){
            return ko.toJSON( self.toJS() );
        };
    };
    
    /* HAMMER VIEW MODEL */
    function HammerViewModel( data ){ //console.dir( data );
        /* our viewmodel */
        
        var self=this,
            urls={ // hard coded urls to the server
                hammer: '/h/',
                item: '/h/item/',
                share: '/h/share/',
                user: '/h/user/'
            },
            _url=function( key, instance ){
                if( urls.hasOwnProperty( key )){
                    if( instance && instance.id() ) return urls[ key ]+instance.id()+'/';
                    return urls[ key ];
                }
            },
            _id_auto_update=function( instance ){
              return function( resp ){
                if( resp.id ) instance.id( resp.id );  
              };  
            };
        data=( data || {});
        self.user=new User( data.user ); /* the current user's info & preferences */
        self.settingsVisible=ko.observable( false );/* toggle the view of the user settings dialog */
        self.hammers=ko.observableArray( $.map( data.hammers, function( h ){/* USER CREATED HAMMERS */
            var hammer=new Hammer( h, self );
            hammer.data.subscribe( function(){
               self.saveHammer( hammer ); 
            });
            return hammer;
        }));
        self.shared_hammers=ko.observableArray( $.map( data.shared, function( s ){/* HAMMERS SHARED WITH USER */
            return new Hammer( s, self );
        }));
        self.selectedHammer=ko.observable();// the hammer being displayed 
        self.tempName=ko.observable();// the name of a new hammer created by user
        
        self.addHammer=function( data ){
            var hammer=new Hammer( data, self );
            self.hammers.push( hammer );
            return hammer;
        };
        
        self.destroyHammer=function( hammer ){
            if( hammer.shared ) return false; // only the creator can delete a hammer
            if( confirm( "Do you want to delete this hammer?")) self.removeHammer( hammer );
        };
        
        self.removeHammer=function( hammer ){
            if( hammer.shared ) return false;
            return $.ajax({
                url: _url( 'hammer', hammer ),
                type: 'delete',
                //data: ko.toJSON({ id: hammer.id(), action: 'delete' })
            }).done( function( resp ){
                if( resp.error ){
                    
                }
                else{
                    self.hammers.remove( hammer );
                    self.selectedHammer(null);
                }
            });
        };
        
        self.removeItem=function( item ){
            return $.ajax({
                url: _url( 'item', item ),
                type: 'delete'
               // data: ko.toJSON({ action: 'delete', id: item.id()})
            });
        };
        self.selectHammer=function( hammer ){
            hammer.tempTitle('');
            self.selectedHammer( hammer );
            store.set( 'selectedHammer', hammer.id());
        };
        self.submitNewHammer=function( form ){ // form was submitted to add hammer
            var input=$( form ).find( 'input[type="text"]'),
                name=input.val();
            if( name ){
                var hammer=self.addHammer({ name: name, can_add: true, can_remove: true, can_change: true, shared: false, creator: self.user.name });
                self.saveHammer( hammer ).done( function( resp ){
                    self.selectHammer( hammer );
                });
                input.val('');
                //self.tempName('');
            }
        };
        self.submitHammer=function( form ){ // form submitted to update existing hammer
            var input=$( form ).find( 'input[type="text"]'),
                hammer=self.selectedHammer(),
                name=input.val();
            if( hammer && name ){
                self.saveHammer( hammer );
            }
            
        };
        self.submitSettings=function( form ){// for was submitted to save user settings
            //form validation here...
            self.saveSettings().done( function( resp ){
              if( resp.error ){
                  console.log( "ERROR", resp.error );
              }  
            });
        };
        self.saveHammer=function( hammer ){
            return $.ajax({
                data: hammer.toJSON(),
                url: _url( 'hammer', hammer ),
                type: hammer.id() ? 'put' : 'post'
            }).done( function( resp ){
                if( resp.id ){
                    hammer.id( resp.id );
                }
            });
        };
        self.saveItem=function( item, hammer ){
            var data=item.toJS();
            data.hammer=hammer.id();
            data.index=hammer.items.indexOf( item );
            console.log( 'index', data.index );
           return $.ajax({
               url: _url( 'item', item ),
               type: item.id() ? 'put' : 'post',
               data: ko.toJSON( data )
            }).done( function( resp ){
                if( resp.id ){ item.id( resp.id ); }
            });
            
            
        };
        self.saveSettings=function(){
          return $.ajax({
              url: _url( 'user' ),
              data: self.user.toJSON()
          });
        };
        self.saveShare=function( share, hammer ){
            var data=ko.toJS( share );
            data.hammer=hammer.id();
           return $.ajax({
               url: _url( 'share', share ),
               data: ko.toJSON( data )
            });
            
        };
        self.toggleSettings=function(){ 
          self.settingsVisible( !self.settingsVisible() );  
        };
        self.unselectHammer=function(){
            if( self.selectedHammer.peek() ){
                self.selectedHammer(null);
                store.set( 'selectedHammer', null);
            }
        };
        
        /* COMPUTED */
        self.hammerStream=ko.computed( function(){// the hammer-entry list in order and filtered based on current user settings
            var hammers=self.hammers(),
                shared=self.shared_hammers(),
                combined=_.union( hammers, shared );
            return combined;
            
        });
        /* UTILITIES */
        var _today=new Date();
        self.formatDate=function( d, fmt ){
          return $.datepicker.formatDate( fmt || self.user.date_format(), d || new Date() );  
        };
        self.dateFormats=[ 'mm d, yy', 'MM d, yy', 'd MM, yy'];
        self.dateFormatOptions=_.map( self.dateFormats, function( f ){
            return { format: f, display: self.formatDate( _today, f ) };
        });
        /* set initially selected hammer */
        var sid=store.get( 'selectedHammer'),
            fn=function( arr ){ return _.find( arr(), function( h ){ return h.id()===sid; });},
            h=sid ? fn( self.hammers ) || fn( self.shared_hammers ) : undefined;
            if( h ){ self.selectHammer( h );}
    }
    
    /* HAMMER EXPOSED AS A PROPERTY OF THE JQUERY OBJECT */
    $.Hammer=function( data ){
        if( !$.Hammer.hammer ){
           ko.applyBindings(  $.Hammer.hammer=new HammerViewModel( data ) );
        }
        return $.Hammer.hammer;
        
    };

    /* DEFAULT AJAX SETTINGS */
    $.ajaxSetup({
        type: 'post',
        dataType:'json',
        url: '/h/',
        contentType: 'application/json'
    });

}( window.jQuery, window.ko, window.store ));
